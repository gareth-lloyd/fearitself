#Save Classifier
def SaveClassifier( classifier):
  fModel = open('BayesModel.pkl',"wb")
  pickle.dump(classifier, fModel,1)
  fModel.close()
  os.system("rm BayesModel.pkl.gz")
  os.system("gzip BayesModel.pkl")

# Load Classifier    
def LoadClassifier( ):
  os.system("gunzip BayesModel.pkl.gz")
  fModel = open('BayesModel.pkl',"rb")
  classifier = pickle.load(fModel)
  fModel.close()
  os.system("gzip BayesModel.pkl")
  return classifier 
