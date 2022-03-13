# ml-sdnids
ml-sdnids使用Ubuntu18.0.4，Python3.9
运行ml-sdnids需要P4的Mininet环境，P4的环境安装和学习参考
https://github.com/jafingerhut/p4-guide
https://github.com/p4lang/tutorials
https://github.com/nsg-ethz/p4-learning

![image](https://user-images.githubusercontent.com/25246938/158066412-1f5335e4-1749-49de-aebd-c37b8e1e5fca.png)

all the program files used in this experiment are listed in detail. The control plane mainly includes realizing the intrusion detection model and the files required for model training. The FeatureExtractor.py file is used primarily in the preprocessing stage of the data set, such as data cleaning, feature extraction, etc. The Autoencoder folder mainly contains files used for the implementation of the autoencoder and model training. The dataset folder contains the dataset used in this experiment. The ocsvm.py file is used to implement the OCSVM algorithm model. The ids_model.py file is used to integrate the autoencoder and OCSVM model used in the anomaly detection module and is responsible for the main intrusion detection functions. The Runtime.py file is responsible for converting the output of the OCSVM model into the flow table required by the data plane. The data plane mainly contains the files necessary for the operation of Mininet and P4 switches. The basic_nids.p4 file is the main file used to simulate P4 switches. It includes five parts: Headers, Parser, Ingress, Egress, and Deparser. The pod-topo folder contains the network topology files that Mininet runs and the configuration files of each switch. Makefile is the configuration file for building the Mininet simulation network. The build folder contains relevant information files generated when the p4 switch is running. The logs and the pcaps folders are the log files generated during the operation of the Mininet simulation network and the traffic captured in the network.
