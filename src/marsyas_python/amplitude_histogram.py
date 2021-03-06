
from bokeh.plotting import figure, show, output_file, vplot
from bokeh import palettes
from bokeh.layouts import column,gridplot
from bokeh.models import ranges
from marsyas_util import create, control2array
import numpy as np
import json
import os
import math
import sys
from sklearn import svm 
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.neural_network import MLPClassifier


from sklearn import preprocessing
from sklearn import metrics
import csv



def histo_plot(mydata, wav_fname): 
    # prepare some data
    y0 = mydata[0,:]


    
    # only plot histogram 
    y0 = y0[0:len(y0)/2]
    
    x = np.array(range(0, len(y0)))

    sum1 = 0.0;
    sum2 = 0.0
    
    for i in range(0, len(y0)/2-4):
        sum1 = sum1 + y0[i];

    for i in range(len(y0)/2+4,len(y0)-1):
        sum2 = sum2 + y0[i];
    # print(sum1/sum2)
    
    # output to static HTML file
    # create a new plot with a title and axis labels
    p = figure(title=wav_fname, x_axis_label=None, y_axis_label=None, 
               plot_height=150, plot_width=400, toolbar_location=None,
               x_range = (150,350))
    
    # add a line renderer with legend and line thickness
    
    p.line(x,y0, legend=str(sum1/sum2) )
    return (p,sum1/sum2,mydata[0,:])


def process_collection(wav_fnames):
    spec = ["Series/plot", 
            ["SoundFileSource/src",
             ["Fanout/fan",
              [
                  ["Series/hist",
                   [
                       "Histogram/histo",
                       "Transposer/trsp",
                       "TextureStats/tstats1"
                       # "Mean/mean1"
                       ]]
                  ,
                  ["Series/dlt",
                   [
                       "Spectrum/spk",
                       "PowerSpectrum/pspk",
                       "MFCC/mfcc", 
                       "TextureStats/tstats2"
                       #"Memory/mem2",
                       #"Mean/mean2"
                   ]]
                  ]]
             ,
             "Transposer/trs"
            ]]
    
    winSize = 512 
    plot_net = create(spec)
#    print(plot_net.toString())
    ratios = [] 
    
    inSamples = plot_net.getControl("mrs_natural/inSamples")
    inSamples.setValue_natural(winSize)
    fname = plot_net.getControl("SoundFileSource/src/mrs_string/filename")
    normalize = plot_net.getControl("Fanout/fan/Series/hist/Histogram/histo/mrs_bool/normalize")
    memSize1 = plot_net.getControl("Fanout/fan/Series/hist/TextureStats/tstats1/mrs_natural/memSize")
    memSize2 = plot_net.getControl("Fanout/fan/Series/dlt/TextureStats/tstats2/mrs_natural/memSize")
#    normalize1 = plot_net.getControl("Fanout/fan/Series/dlt/Histogram/histo1/mrs_bool/normalize")


    memSize1.setValue_natural(200);
    memSize2.setValue_natural(200);
    reset = plot_net.getControl("Fanout/fan/Series/hist/Histogram/histo/mrs_bool/reset")
#    reset1 = plot_net.getControl("Fanout/fan/Series/dlt/Histogram/histo1/mrs_bool/reset")        
    figs = []
    ratio = 0.0
    avg_ratio = 0.0
    num_glitch = 0
    numFiles = 0
    seconds2process = 15.0
    samples2process = seconds2process * 8000
    iterations2process = int(samples2process * 1.0 / winSize)




    for wav_fname in wav_fnames:
        print(str(numFiles) + ' - ' +  wav_fname);
        fname.setValue_string(wav_fname)
        reset.setValue_bool(True)
#        reset1.setValue_bool(True)
        
        nTicks = 0
        for i in range(0, iterations2process): 
            # while plot_net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
        
            plot_net.tick()
            nTicks = nTicks + 1
        normalize.setValue_bool(True)
        # normalize1.setValue_bool(True)
        # extra tick to normalize 
        plot_net.tick()
        
        mydata = control2array(plot_net, "mrs_realvec/processedData")
        (fig, ratio, histo) = histo_plot(mydata, wav_fname)
        ratios.append(histo)
        #ratios.append(np.array([ratio, ratio]))
        figs.append(fig)
        numFiles = numFiles + 1;
#        avg_ratio = avg_ratio + abs(1.0-ratio)
#        if (abs(1.0-ratio) > 0.2):
#           num_glitch = num_glitch+1 

#    avg_ratio = avg_ratio / numFiles
#    print(("AVERAGE RATIO=" , avg_ratio))
#    print(("GLITCH PERCENTAGE=", int(100 * (num_glitch * 1.0/len(wav_fnames)))))
#    show(gridplot(*figs, ncols=2))
    return (ratios, wav_fnames)



def main(): 

    #playlist_folder = "/Users/georgetzanetakis/data/sound/nonglitch/"
    #playlist_folder = "/Users/georgetzanetakis/data/sound/glitch/"
    #playlist_folder = "/Users/georgetzanetakis/data/sound/normal/"
    #playlist_folder = "/tmp/smule_songs1/"    
    #playlist_folder = "/Users/georgetzanetakis/data/sound/headphones/"
    #playlist_folder = "/Users/georgetzanetakis/data/sound/2017/"
    #playlist_folder = "/Users/georgetzanetakis/data/sound/2016/"
    positive_folder = sys.argv[1]
    negative_folder = sys.argv[2]
    test_folder = sys.argv[3]


    output_file("positive_histograms.html")

    wav_fnames = [f for f in os.listdir(positive_folder) if f.endswith(".wav")]
    wav_fnames = [positive_folder + s for s in wav_fnames]
    (pos_ratios, pos_names) = process_collection(wav_fnames)
    
    pfeatures = np.asarray(pos_ratios)
    print(pfeatures.shape)
    ptruth = np.ones(len(pos_ratios))
    print(ptruth.shape)
    output_file("negative_histograms.html")

    wav_fnames = [f for f in os.listdir(negative_folder) if f.endswith(".wav")]
    wav_fnames = [negative_folder + s for s in wav_fnames]    
    (neg_ratios, neg_names) = process_collection(wav_fnames);
    
    nfeatures = np.asarray(neg_ratios)
    print(nfeatures.shape)    
    ntruth = np.zeros(len(neg_ratios))
    print(ntruth.shape)
    X = np.concatenate([pos_ratios, neg_ratios])
    print(X.shape)
    y = np.concatenate([ptruth,ntruth])
    print(y.shape)


    csv_fname = "glitch_other.csv" 
    with open(csv_fname, 'rb') as f:
        reader = csv.reader(f)
        i = 0
        wav_fnames = [] 
        for row in reader:
            wav_fnames.append(test_folder + row[0] + '.wav')
    print(wav_fnames)
    # wav_fnames = [f for f in os.listdir(test_folder) if f.endswith(".wav")]
    # wav_fnames = [test_folder + s for s in wav_fnames]
    
    (test_ratios, test_names) = process_collection(wav_fnames)
    
    Xtest = np.concatenate([test_ratios])
    print("XTEST", Xtest.shape)
    min_max_scaler = preprocessing.MinMaxScaler()
    X = min_max_scaler.fit_transform(X)
    Xtest = min_max_scaler.transform(Xtest)
    
    clf = svm.SVC(kernel='linear', C=1)
#    clf = svm.SVC(kernel='linear', C=0.025)
#    clf = svm.SVC(gamma = 2, C=1)
    clf.fit(X,y)
    
    scores = cross_val_score(clf, X, y, cv=30)
    predicted = cross_val_predict(clf, X, y, cv=30)
    cm = metrics.confusion_matrix(y, predicted)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print(cm)
    print("SUPPORT VECTOR MACHINE")
    print(scores)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    i = 0
    glitches = 0
    for prediction in clf.predict(Xtest):
        print(prediction, test_names[i])
        print(prediction)
        if (prediction == 1):
            glitches = glitches + 1 
        i = i + 1
    print(glitches, i)

    rclf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
    rclf.fit(X,y)
    rscores = cross_val_score(rclf, X, y, cv=30)
    print("RANDOM FOREST")    
    print(rscores)
    print("Accuracy: %0.2f (+/- %0.2f)" % (rscores.mean(), rscores.std() * 2))  


    mclf =  MLPClassifier(alpha=1)
    mclf.fit(X,y)
    mscores = cross_val_score(rclf, X, y, cv=30)
    print("Multilayer Perceptron")    
    print(mscores)
    print("Accuracy: %0.2f (+/- %0.2f)" % (mscores.mean(), mscores.std() * 2))  


    
    dclf = DummyClassifier(strategy='most_frequent',random_state=0)
    dclf.fit(X,y)
    dscores = cross_val_score(dclf, X, y, cv=30)
    print(dscores)
    print("Accuracy: %0.2f (+/- %0.2f)" % (dscores.mean(), dscores.std() * 2))    
    
    

if __name__ == "__main__":
   main()

