import sys
import time
import numpy as np
import lightgbm as lgb
from os.path import join
from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix, accuracy_score

class MSLR:
	def __init__(self):
		self.DIR = "../../../MSLR-WEB10K/Fold1/"

	def train_file(self):
		return join(self.DIR, 'train.txt')

	def test_file(self):
		return join(self.DIR, 'test.txt')

	def validation_file(self):
		return join(self.DIR, 'vali.txt')

	def svm_file(self):
		return join(self.DIR, 'trained_svm.txt')

	def filter(self):
		return list(range(2, 102))

	def get_data(self, file, LIMIT=sys.maxsize, LIMIT_Z = sys.maxsize):
		x = []
		y = []
		L = 0
		Z = 0
		O = 0
		with open(file, 'r') as f:
			for line in f:
				if L < LIMIT:
					l = line.strip().split()
					y_v = (lambda x: 1 if x >= 2 else 0)(int(l[0]))
					if Z < LIMIT_Z and y_v == 0:
						y.append(y_v)
						Z += 1
						x.append([float(tok.split(":")[1]) for tok in [l[i] for i in self.filter()]])
					if y_v == 1:
						y.append(y_v)
						x.append([float(tok.split(":")[1]) for tok in [l[i] for i in self.filter()]])
						O += 1

					L += 1

		print(str(Z) + " " + str(O))
		X = np.array(x)
		y = np.array(y)

		print(X.shape)
		print(y.shape)

		return X, y

	def train_lightgbm(self, X_train , y_train, X_test, y_test):

		# create dataset for lightgbm
		lgb_train = lgb.Dataset(X_train, y_train)
		lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

		# specify your configurations as a dict
		params = {
			'task': 'train',
			'boosting_type': 'gbdt',
			'objective': 'multiclass',
			'metric': 'multi_logloss',
			'num_class': 2,
			'metric_freq': 1,
			'is_training_metric': True,
			'early_stopping': 10,
			'num_trees': 100,
			'num_leaves': 31,
			'learning_rate': 0.05,
			'verbose': 0
		}

		# train
		gbm = lgb.train(params,
						lgb_train,
						num_boost_round=20,
						valid_sets=lgb_eval,
						early_stopping_rounds=5)
		return gbm


def test_lightgbm(gbm, X_test, y_test):

	print('Start predicting...')

	y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
	# print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)

	y_pred = [max([0, 1], key=lambda x: val[x]) for val in y_pred]
	print('The accuracy of prediction is:', accuracy_score(y_test, y_pred))
	cmatrix = confusion_matrix(y_test, y_pred)
	print(cmatrix)


def test_standard_models(mslr, X_train, y_train, X_test, y_test):

	clf = mslr.train_NN(X_train, y_train)
	joblib.dump(clf, mslr.svm_file())
	y_pred = clf.predict(X_test)
	cmatrix = confusion_matrix(y_test, y_pred)
	print(cmatrix)
	print("test score --> " + str(clf.score(X_test, y_test)))


if __name__ == "__main__":


	init = time.time()
	mslr = MSLR()
	min_max_scaler = preprocessing.MinMaxScaler()  # http://scikit-learn.org/stable/modules/preprocessing.html
	# pca = decomposition.PCA(n_components=77) # nope

	print("Collecting train data")
	X_train, y_train = mslr.get_data(mslr.train_file())
	X_train = min_max_scaler.fit_transform(X_train)
	# X_train = pca.fit(X_train).transform(X_train)


	print(time.time() - init)
	init = time.time()

	print("Collecting cross validation data")
	X_cross, y_cross = mslr.get_data(mslr.validation_file())
	X_cross = min_max_scaler.fit_transform(X_cross)
	# X_cross = pca.fit(X_cross).transform(X_cross)

	print("Collecting test data")
	X_test, y_test = mslr.get_data(mslr.test_file())
	X_test = min_max_scaler.fit_transform(X_test)
	# X_test = pca.fit(X_test).transform(X_test)

	print(time.time() - init)
	print("Finished collecting data")

	print("---------------------")

	print("Start Training")
	gbm = mslr.train_lightgbm(X_train, y_train, X_test, y_test)
	# gbm.save_model(mslr.svm_file()) # save model
	# bst = lgb.Booster(mslr.svm_file()) # load model

	test_lightgbm(gbm,  X_test, y_test)
	test_lightgbm(gbm, X_cross, y_cross)
