#!/usr/bin/env python3
#
# This code is licensed under GNU GPL v2.0 or higher. Please see LICENSE for details.
#
#
# Output of Brainome Daimensions(tm) Table Compiler v0.8.
# Compile time: Feb-28-2020 22:25:34
# Invocation: btc Data/nomao.csv -o Models/nomao.py -v -v -v -stopat 97.52 -port 8090 -e 9 -target Class -cm {'1':0,'2':1}
# This source code requires Python 3.
#
"""
System Type:                        Binary classifier
Best-guess accuracy:                71.43%
Model accuracy:                     94.96% (32728/34465 correct)
Improvement over best guess:        23.53% (of possible 28.57%)
Model capacity (MEC):               241 bits
Generalization ratio:               135.80 bits/bit
Model efficiency:                   0.09%/parameter
System behavior
True Negatives:                     26.02% (8968/34465)
True Positives:                     68.94% (23760/34465)
False Negatives:                    2.50% (861/34465)
False Positives:                    2.54% (876/34465)
True Pos. Rate/Sensitivity/Recall:  0.97
True Neg. Rate/Specificity:         0.91
Precision:                          0.96
F-1 Measure:                        0.96
False Negative Rate/Miss Rate:      0.03
Critical Success Index:             0.93
"""

# Imports -- Python3 standard library
import sys
import math
import os
import argparse
import tempfile
import csv
import binascii
import faulthandler


# Magic constants follow
# I/O buffer for clean. Reduce this constant for low memory devices. 
IOBUF=100000000

# Ugly workaround for large classifiers
sys.setrecursionlimit(1000000)

# Training file given to compiler
TRAINFILE="nomao.csv"


#Number of output logits
num_output_logits = 1

#Number of attributes
num_attr = 118

# Preprocessor for CSV files
def clean(filename, outfile, rounding=-1, headerless=False, testfile=False):
    
    clean.classlist=[]
    clean.testfile=testfile
    clean.mapping={}
    clean.mapping={'1':0,'2':1}

    def convert(cell):
        value=str(cell)
        try:
            result=int(value)
            return result
        except:
            try:
                result=float(value)
                if (rounding!=-1):
                    result=int(result*math.pow(10,rounding))/math.pow(10,rounding)
                return result
            except:
                result=(binascii.crc32(value.encode('utf8')) % (1<<32))
                return result

    def convertclassid(cell):
        if (clean.testfile):
            return convert(cell)
        value=str(cell)
        if (value==''):
            raise ValueError("All cells in the target column must contain a class label.")

        if (not clean.mapping=={}):
            result=-1
            try:
                result=clean.mapping[cell]
            except:
                raise ValueError("Class label '"+value+"' encountered in input not defined in user-provided mapping.")
            if (not (result==0 or result==1)):
                raise ValueError("Alpha version restriction: Class labels must be mapped to 0 and 1.")
            if (not str(result) in clean.classlist):
                clean.classlist=clean.classlist+[str(result)]
            return result
        try:
            result=float(cell)
            if (rounding!=-1):
                result=int(result*math.pow(10,rounding))/math.pow(10,rounding)
            else:
                result=int(result)

            if (not str(result) in clean.classlist):
                clean.classlist=clean.classlist+[str(result)]
        except:
            result=(binascii.crc32(value.encode('utf8')) % (1<<32))
            if (result in clean.classlist):
                result=clean.classlist.index(result)
            else:
                clean.classlist=clean.classlist+[result]
                result=clean.classlist.index(result)
            if (not (result==0 or result==1)):
                raise ValueError("Alpha version restriction: Class labels must be mappable to 0 and 1.")
        finally:
            if (result<0 or result>1):
                raise ValueError("Alpha version restriction: Integer class labels can only be 0 or 1.")
        return result

    rowcount=0
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        f=open(outfile,"w+")
        if (headerless==False):
            next(reader,None)
        outbuf=[]
        for row in reader:
            if (row==[]):  # Skip empty rows
                continue
            rowcount=rowcount+1
            rowlen=num_attr
            if (not testfile):
                rowlen=rowlen+1    
            if (not len(row)==rowlen):
                raise ValueError("Column count must match trained predictor. Row "+str(rowcount)+" differs.")
            i=0
            for elem in row:
                if(i+1<len(row)):
                    outbuf.append(str(convert(elem)))
                    outbuf.append(',')
                else:
                    classid=str(convertclassid(elem))
                    outbuf.append(classid)
                i=i+1
            if (len(outbuf)<IOBUF):
                outbuf.append("\n")
            else:
                print(''.join(outbuf), file=f)
                outbuf=[]
        print(''.join(outbuf),end="", file=f)
        f.close()

        if (testfile==False and not len(clean.classlist)==2):
            raise ValueError("Number of classes must be 2.")


# Helper (save an import)
def argmax(l):
    f = lambda i: l[i]
    return max(range(len(l)), key=f)

# Classifier
def classify(row):
    x=row
    h_0 = max((((0.53333247 * float(x[0]))+ (0.31594977 * float(x[1]))+ (0.1111196 * float(x[2]))+ (-0.06316057 * float(x[3]))+ (0.3324651 * float(x[4]))+ (-0.031473648 * float(x[5]))+ (0.6673645 * float(x[6]))+ (0.81119245 * float(x[7]))+ (-0.43508312 * float(x[8]))+ (0.38920346 * float(x[9]))+ (-0.14874406 * float(x[10]))+ (-0.06457392 * float(x[11]))+ (0.6474092 * float(x[12]))+ (-1.0587679 * float(x[13]))+ (-1.1223375 * float(x[14]))+ (-1.2561592 * float(x[15]))+ (0.47682536 * float(x[16]))+ (0.36901036 * float(x[17]))+ (0.5312494 * float(x[18]))+ (0.7600062 * float(x[19]))+ (0.39000437 * float(x[20]))+ (-0.2736404 * float(x[21]))+ (0.26387864 * float(x[22]))+ (-1.0606309 * float(x[23]))+ (0.15268296 * float(x[24]))+ (-0.82737935 * float(x[25]))+ (0.7459823 * float(x[26]))+ (-0.080326594 * float(x[27]))+ (-0.30981794 * float(x[28]))+ (-0.58708847 * float(x[29]))+ (0.28599122 * float(x[30]))+ (-0.35017556 * float(x[31]))+ (-0.0537176 * float(x[32]))+ (-1.1295184 * float(x[33]))+ (0.04951061 * float(x[34]))+ (0.045657765 * float(x[35]))+ (0.06126718 * float(x[36]))+ (0.7260607 * float(x[37]))+ (0.13724051 * float(x[38]))+ (-0.5073849 * float(x[39]))+ (-0.3049131 * float(x[40]))+ (0.2162854 * float(x[41]))+ (-1.0817008 * float(x[42]))+ (0.14122993 * float(x[43]))+ (0.13932225 * float(x[44]))+ (-0.7715227 * float(x[45]))+ (-1.0336686 * float(x[46]))+ (-0.66066456 * float(x[47]))+ (-0.5007922 * float(x[48]))+ (-0.087723054 * float(x[49])))+ ((-0.351158 * float(x[50]))+ (0.7485926 * float(x[51]))+ (-1.0241671 * float(x[52]))+ (-0.81029326 * float(x[53]))+ (-1.365032 * float(x[54]))+ (-0.3814344 * float(x[55]))+ (-0.5829709 * float(x[56]))+ (-0.14736326 * float(x[57]))+ (-0.6390512 * float(x[58]))+ (-0.7707133 * float(x[59]))+ (-0.95214736 * float(x[60]))+ (0.1729055 * float(x[61]))+ (-1.1781026 * float(x[62]))+ (-1.0654756 * float(x[63]))+ (-0.40682015 * float(x[64]))+ (0.50454444 * float(x[65]))+ (-0.9555755 * float(x[66]))+ (0.5347837 * float(x[67]))+ (-0.98881114 * float(x[68]))+ (0.81611526 * float(x[69]))+ (-0.35462964 * float(x[70]))+ (0.66158766 * float(x[71]))+ (-0.016921237 * float(x[72]))+ (0.25191614 * float(x[73]))+ (-1.1507553 * float(x[74]))+ (-0.66214365 * float(x[75]))+ (-0.98873866 * float(x[76]))+ (-0.6354772 * float(x[77]))+ (-1.4477737 * float(x[78]))+ (-1.0492629 * float(x[79]))+ (-0.4012981 * float(x[80]))+ (-1.1015291 * float(x[81]))+ (0.15512013 * float(x[82]))+ (-0.0966212 * float(x[83]))+ (-0.6990451 * float(x[84]))+ (-0.183328 * float(x[85]))+ (-1.5013533 * float(x[86]))+ (-0.5373413 * float(x[87]))+ (0.964815 * float(x[88]))+ (-0.4818681 * float(x[89]))+ (0.312334 * float(x[90]))+ (-1.1361126 * float(x[91]))+ (0.31083268 * float(x[92]))+ (-0.59603226 * float(x[93]))+ (-0.78236336 * float(x[94]))+ (-0.056798223 * float(x[95]))+ (-0.88694924 * float(x[96]))+ (0.768114 * float(x[97]))+ (-0.83111924 * float(x[98]))+ (0.07580531 * float(x[99])))+ ((-0.6890987 * float(x[100]))+ (0.43806365 * float(x[101]))+ (0.99073035 * float(x[102]))+ (-0.7944113 * float(x[103]))+ (-0.07719351 * float(x[104]))+ (0.10749833 * float(x[105]))+ (0.16683108 * float(x[106]))+ (-0.8457543 * float(x[107]))+ (0.6818864 * float(x[108]))+ (-0.21613386 * float(x[109]))+ (0.65736395 * float(x[110]))+ (0.4198807 * float(x[111]))+ (-0.6284456 * float(x[112]))+ (0.50722635 * float(x[113]))+ (-0.25057596 * float(x[114]))+ (0.7831285 * float(x[115]))+ (-0.06727252 * float(x[116]))+ (0.54121876 * float(x[117]))) + -0.13219713), 0)
    h_1 = max((((0.39696994 * float(x[0]))+ (-1.009744 * float(x[1]))+ (-0.49672803 * float(x[2]))+ (2.4473562 * float(x[3]))+ (-1.0303057 * float(x[4]))+ (2.1545048 * float(x[5]))+ (0.3695135 * float(x[6]))+ (-0.7484104 * float(x[7]))+ (-0.5947868 * float(x[8]))+ (-0.74263835 * float(x[9]))+ (-0.673985 * float(x[10]))+ (0.9776379 * float(x[11]))+ (0.7172738 * float(x[12]))+ (0.58302605 * float(x[13]))+ (1.0956279 * float(x[14]))+ (-1.2262381 * float(x[15]))+ (0.7314209 * float(x[16]))+ (1.150789 * float(x[17]))+ (-0.54220253 * float(x[18]))+ (-1.0457014 * float(x[19]))+ (-0.17251028 * float(x[20]))+ (-0.6421088 * float(x[21]))+ (0.5887748 * float(x[22]))+ (-0.68722665 * float(x[23]))+ (0.85298824 * float(x[24]))+ (-0.57400477 * float(x[25]))+ (-0.7094606 * float(x[26]))+ (-0.16033424 * float(x[27]))+ (0.027330315 * float(x[28]))+ (1.1634775 * float(x[29]))+ (-0.18395483 * float(x[30]))+ (0.21638615 * float(x[31]))+ (-0.36028573 * float(x[32]))+ (-2.0495255 * float(x[33]))+ (-0.38106248 * float(x[34]))+ (0.14924102 * float(x[35]))+ (-0.37491694 * float(x[36]))+ (2.525031 * float(x[37]))+ (0.9445663 * float(x[38]))+ (-0.67719835 * float(x[39]))+ (-0.8684869 * float(x[40]))+ (-0.22702569 * float(x[41]))+ (0.7758773 * float(x[42]))+ (-0.8295272 * float(x[43]))+ (0.25220805 * float(x[44]))+ (0.45156488 * float(x[45]))+ (-0.47596467 * float(x[46]))+ (0.6803588 * float(x[47]))+ (-0.6848028 * float(x[48]))+ (0.846396 * float(x[49])))+ ((-1.0723846 * float(x[50]))+ (-0.6512376 * float(x[51]))+ (1.1175517 * float(x[52]))+ (0.4461116 * float(x[53]))+ (-1.3463773 * float(x[54]))+ (0.97031546 * float(x[55]))+ (-0.40941128 * float(x[56]))+ (-1.6905236 * float(x[57]))+ (1.5397851 * float(x[58]))+ (2.9200938 * float(x[59]))+ (-2.8877122 * float(x[60]))+ (1.3483313 * float(x[61]))+ (-0.014648248 * float(x[62]))+ (-0.5125456 * float(x[63]))+ (0.57245034 * float(x[64]))+ (-0.082010284 * float(x[65]))+ (-2.565785 * float(x[66]))+ (1.0443591 * float(x[67]))+ (-3.002499 * float(x[68]))+ (3.4183972 * float(x[69]))+ (-0.2414124 * float(x[70]))+ (0.3237825 * float(x[71]))+ (-0.26738185 * float(x[72]))+ (-2.139651 * float(x[73]))+ (-1.9842418 * float(x[74]))+ (2.188534 * float(x[75]))+ (1.0421873 * float(x[76]))+ (0.73364216 * float(x[77]))+ (0.89095783 * float(x[78]))+ (-0.6617683 * float(x[79]))+ (0.3278541 * float(x[80]))+ (0.77062494 * float(x[81]))+ (-0.5315963 * float(x[82]))+ (-0.06073161 * float(x[83]))+ (0.32028788 * float(x[84]))+ (-0.6215045 * float(x[85]))+ (-0.19245942 * float(x[86]))+ (0.23482046 * float(x[87]))+ (0.8032372 * float(x[88]))+ (-0.5671405 * float(x[89]))+ (1.7337723 * float(x[90]))+ (0.59043235 * float(x[91]))+ (0.12256166 * float(x[92]))+ (0.9590185 * float(x[93]))+ (0.85795736 * float(x[94]))+ (-0.42277655 * float(x[95]))+ (0.9564523 * float(x[96]))+ (2.4213362 * float(x[97]))+ (-1.870063 * float(x[98]))+ (0.8961785 * float(x[99])))+ ((-1.425269 * float(x[100]))+ (0.39207435 * float(x[101]))+ (0.82816726 * float(x[102]))+ (-0.17683005 * float(x[103]))+ (0.9142888 * float(x[104]))+ (0.9611904 * float(x[105]))+ (-0.13205963 * float(x[106]))+ (-1.0237279 * float(x[107]))+ (-0.14404184 * float(x[108]))+ (0.1337429 * float(x[109]))+ (-0.19315434 * float(x[110]))+ (0.3685789 * float(x[111]))+ (0.38599238 * float(x[112]))+ (0.7994086 * float(x[113]))+ (-0.1992545 * float(x[114]))+ (-0.33172917 * float(x[115]))+ (0.6129259 * float(x[116]))+ (-0.15196739 * float(x[117]))) + -1.0638636), 0)
    o_0 = (0.3717811 * h_0)+ (2.3028653 * h_1) + -6.326208
             
    if num_output_logits==1:
        return o_0>=0
    else:
        return argmax([eval('o'+str(i)) for i in range(num_output_logits)])

# Main method
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predictor trained on '+TRAINFILE)
    parser.add_argument('csvfile', type=str, help='CSV file containing test set (unlabeled).')
    parser.add_argument('-validate', action='store_true', help='Validation mode. csvfile must be labeled. Output is classification statistics rather than predictions.')
    parser.add_argument('-cleanfile',action='store_true',help='Use this flag to save prediction time if the csvfile you are passing has already been preprocessed. Implies headerless.')
    parser.add_argument('-headerless', help='Do not treat the first line of csvfile as a header.', action='store_true')
    args = parser.parse_args()
    faulthandler.enable()
    
    if not args.validate: # Then predict
        if args.cleanfile:
            with open(args.csvfile,'r') as cleancsvfile:
                cleancsvreader = csv.reader(cleancsvfile)
                for cleanrow in cleancsvreader:
                    if len(cleanrow)==0:
                        continue
                print(str(','.join(str(j) for j in ([i for i in cleanrow])))+','+str(int(classify(cleanrow))))
        else:
            tempdir=tempfile.gettempdir()
            cleanfile=tempdir+os.sep+"clean.csv"
            clean(args.csvfile,cleanfile, -1, args.headerless, True)
            with open(cleanfile,'r') as cleancsvfile, open(args.csvfile,'r') as dirtycsvfile:
                cleancsvreader = csv.reader(cleancsvfile)
                dirtycsvreader = csv.reader(dirtycsvfile)
                if (not args.headerless):
                        print(','.join(next(dirtycsvreader, None)+['Prediction']))
                for cleanrow,dirtyrow in zip(cleancsvreader,dirtycsvreader):
                    if len(cleanrow)==0:
                        continue
                    print(str(','.join(str(j) for j in ([i for i in dirtyrow])))+','+str(int(classify(cleanrow))))
            os.remove(cleanfile)
            
    else: # Then validate this predictor
        tempdir=tempfile.gettempdir()
        temp_name = next(tempfile._get_candidate_names())
        cleanvalfile=tempdir+os.sep+temp_name
        clean(args.csvfile,cleanvalfile, -1, args.headerless)
        with open(cleanvalfile,'r') as valcsvfile:
            count,correct_count,num_TP,num_TN,num_FP,num_FN,num_class_1,num_class_0=0,0,0,0,0,0,0,0
            valcsvreader = csv.reader(valcsvfile)
            for valrow in valcsvreader:
                if len(valrow)==0:
                    continue
                if int(classify(valrow[:-1]))==int(float(valrow[-1])):
                    correct_count+=1
                    if int(float(valrow[-1]))==1:
                        num_class_1+=1
                        num_TP+=1
                    else:
                        num_class_0+=1
                        num_TN+=1
                else:
                    if int(float(valrow[-1]))==1:
                        num_class_1+=1
                        num_FN+=1
                    else:
                        num_class_0+=1
                        num_FP+=1
                count+=1

        model_cap=241

        FN=float(num_FN)*100.0/float(count)
        FP=float(num_FP)*100.0/float(count)
        TN=float(num_TN)*100.0/float(count)
        TP=float(num_TP)*100.0/float(count)
        num_correct=correct_count

        if int(num_TP+num_FN)!=0:
            TPR=num_TP/(num_TP+num_FN) # Sensitivity, Recall
        if int(num_TN+num_FP)!=0:
            TNR=num_TN/(num_TN+num_FP) # Specificity, 
        if int(num_TP+num_FP)!=0:
            PPV=num_TP/(num_TP+num_FP) # Recall
        if int(num_FN+num_TP)!=0:
            FNR=num_FN/(num_FN+num_TP) # Miss rate
        if int(2*num_TP+num_FP+num_FN)!=0:
            FONE=2*num_TP/(2*num_TP+num_FP+num_FN) # F1 Score
        if int(num_TP+num_FN+num_FP)!=0:
            TS=num_TP/(num_TP+num_FN+num_FP) # Critical Success Index

        randguess=int(float(10000.0*max(num_class_1,num_class_0))/count)/100.0
        modelacc=int(float(num_correct*10000)/count)/100.0

        print("System Type:                        Binary classifier")
        print("Best-guess accuracy:                {:.2f}%".format(randguess))
        print("Model accuracy:                     {:.2f}%".format(modelacc)+" ("+str(int(num_correct))+"/"+str(count)+" correct)")
        print("Improvement over best guess:        {:.2f}%".format(modelacc-randguess)+" (of possible "+str(round(100-randguess,2))+"%)")
        print("Model capacity (MEC):               {:.0f} bits".format(model_cap))
        print("Generalization ratio:               {:.2f}".format(int(float(num_correct*100)/model_cap)/100.0)+" bits/bit")
        print("Model efficiency:                   {:.2f}%/parameter".format(int(100*(modelacc-randguess)/model_cap)/100.0))
        print("System behavior")
        print("True Negatives:                     {:.2f}%".format(TN)+" ("+str(int(num_TN))+"/"+str(count)+")")
        print("True Positives:                     {:.2f}%".format(TP)+" ("+str(int(num_TP))+"/"+str(count)+")")
        print("False Negatives:                    {:.2f}%".format(FN)+" ("+str(int(num_FN))+"/"+str(count)+")")
        print("False Positives:                    {:.2f}%".format(FP)+" ("+str(int(num_FP))+"/"+str(count)+")")
        if int(num_TP+num_FN)!=0:
            print("True Pos. Rate/Sensitivity/Recall:  {:.2f}".format(TPR))
        if int(num_TN+num_FP)!=0:
            print("True Neg. Rate/Specificity:         {:.2f}".format(TNR))
        if int(num_TP+num_FP)!=0:
            print("Precision:                          {:.2f}".format(PPV))
        if int(2*num_TP+num_FP+num_FN)!=0:
            print("F-1 Measure:                        {:.2f}".format(FONE))
        if int(num_TP+num_FN)!=0:
            print("False Negative Rate/Miss Rate:      {:.2f}".format(FNR))
        if int(num_TP+num_FN+num_FP)!=0:    
            print("Critical Success Index:             {:.2f}".format(TS))


        os.remove(cleanvalfile)

