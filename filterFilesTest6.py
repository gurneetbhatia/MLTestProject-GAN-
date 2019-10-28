import pickle

filenames = pickle.load(open("filenames.p", 'rb'))
correctFilenames = []
for filename in filenames:
    if not filename.split('_')[-1][:-4] == "format0":
        correctFilenames.append(filename)
#pickle.dump(correctFilenames, open('filenames.p', 'wb'))
