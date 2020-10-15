from keras.models import load_model
import pandas as pd
from utils import data_utils
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from optparse import OptionParser
from matplotlib import pyplot as plt
import os
import shutil


predict_date = '2014/4/1'
data_base = pd.read_csv('label_data_web.csv')
time_step = 19
columns = 5
col_n = ['shoupanjia', 'zuigaojia', 'zuidijia', 'chengjiaojine', 'num']
dataset = pd.DataFrame(data_base, columns=col_n).values
date_list = pd.DataFrame(data_base, columns=['date']).values
xs = [d[0] for d in date_list]
sc = MinMaxScaler(feature_range=(0, 1))


def test_data(pos):
    global predict_date, time_step
    training_set_scaled = sc.fit_transform(dataset)
    X_test = []
    X_test.append(training_set_scaled[pos - time_step + 1:pos + 1, :])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], columns))
    return X_test


def main():
    global predict_date, time_step
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-e", "--epochs", action="store", type="int", dest="epochs")
    parser.add_option("-t", "--time_step", action="store", type="int", dest="time_step")
    parser.add_option("-m", "--model_base", action="store", type="string", dest="model_base")
    parser.add_option("-d", "--date", action="store", type="string", dest="test_date")
    (options, args) = parser.parse_args()
    predict_date = options.test_date
    time_step = options.time_step
    epochs = options.epochs
    model_base = options.model_base
    out_tag = 'ts%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_5 = 'n5_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_10 = 'n10_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_19 = 'n19_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_40 = 'n40_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_60 = 'n60_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_90 = 'n90_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_120 = 'n120_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    tag_240 = 'n240_t%d_e%d_%s' % (time_step, epochs, data_utils.get_tag_date(predict_date))
    pos = data_utils.get_divide_pos(xs, predict_date)
    pos = pos
    print(pos)
    end = pos + 240 + 20
    X_test = test_data(pos)
    print(X_test.shape)

    predict_model_5 = load_model('%s/%s/model.h5' % (model_base, tag_5))
    predict_model_10 = load_model('%s/%s/model.h5' % (model_base, tag_10))
    predict_model_19 = load_model('%s/%s/model.h5' % (model_base, tag_19))
    predict_model_40 = load_model('%s/%s/model.h5' % (model_base, tag_40))
    predict_model_60 = load_model('%s/%s/model.h5' % (model_base, tag_60))
    predict_model_90 = load_model('%s/%s/model.h5' % (model_base, tag_90))
    predict_model_120 = load_model('%s/%s/model.h5' % (model_base, tag_120))
    predict_model_240 = load_model('%s/%s/model.h5' % (model_base, tag_240))

    predicted_5 = predict_model_5.predict(X_test)
    predicted_10 = predict_model_10.predict(X_test)
    predicted_19 = predict_model_19.predict(X_test)
    predicted_40 = predict_model_40.predict(X_test)
    predicted_60 = predict_model_60.predict(X_test)
    predicted_90 = predict_model_90.predict(X_test)
    predicted_120 = predict_model_120.predict(X_test)
    predicted_240 = predict_model_240.predict(X_test)

    origin_data_5 = sc.inverse_transform(predicted_5)
    origin_data_10 = sc.inverse_transform(predicted_10)
    origin_data_19 = sc.inverse_transform(predicted_19)
    origin_data_40 = sc.inverse_transform(predicted_40)
    origin_data_60 = sc.inverse_transform(predicted_60)
    origin_data_90 = sc.inverse_transform(predicted_90)
    origin_data_120 = sc.inverse_transform(predicted_120)
    origin_data_240 = sc.inverse_transform(predicted_240)
    #np.savetxt('predict_60.txt', origin_data)
    start_line = dataset[pos]
    print(start_line)
    print(origin_data_5)
    predict_list = list()
    print(type(dataset[pos, 0]))
    #print(origin_data_20)
    #print(type(origin_data_20[0, 0]))
    predict_list.append(dataset[pos, 0])
    predict_list.append(origin_data_5[0, 0])
    predict_list.append(origin_data_10[0, 0])
    predict_list.append(origin_data_19[0, 0])
    predict_list.append(origin_data_40[0, 0])
    predict_list.append(origin_data_60[0, 0])
    predict_list.append(origin_data_90[0, 0])
    predict_list.append(origin_data_120[0, 0])
    predict_list.append(origin_data_240[0, 0])
    print(predict_list)
    index_list = [0, 5, 10, 19, 40, 60, 90, 120, 240]
    #plt.plot(dataset[pos: end, 0], color='black', label='Stock Price')
    plt.plot(index_list, predict_list, color='green', label='Test Price')
    xticks = list()
    ##xticks.append(date_list[pos, 0])
    #xticks.append(date_list[pos + 20, 0])
    xticks.append('0')
    xticks.append('5')
    xticks.append('10')
    xticks.append('19')
    xticks.append('40')
    xticks.append('60')
    xticks.append('90')
    xticks.append('120')
    xticks.append('240')
    #xticks.append(date_list[pos + 20, 0])
    #xticks.append(date_list[pos + 60, 0])
    #xticks.append(date_list[pos + 90, 0])
    #xticks.append(date_list[pos + 120, 0])
    #xticks.append(date_list[pos + 240, 0])
    plt.xticks(index_list, xticks, rotation=25)
    plt.title(out_tag)
    src_path = '/opt/work/stock/pic_8p/%s-release-8P.png' % out_tag
    dist_path = '/opt/web/stock_web/static/%s-release-8P.png' % out_tag
    plt.savefig(src_path)
    shutil.copy(src_path, dist_path)
    #np.savetxt('20.txt', origin_data_20)
    #np.savetxt('60.txt', origin_data_60)
    #np.savetxt('90.txt', origin_data_90)
    #np.savetxt('120.txt', origin_data_120)
    #np.savetxt('240.txt', origin_data_240)


if __name__ == '__main__':
    main()
