# Dolabra: A Syslog NER Tool

Dolabra, a roman pickaxe, is the tool of choice for applying NER ( Named Entity Recognition ) to syslog messages, specifically network device syslog. 

By supplying training logs and the feature location you would like to begin recognizing, Dolabra will train an NER pipeline model with spaCy and make this model available via REST api (currently) or message bus ETL ( in-progress ). It will dig through logs supplied and return the entities recognized.

## Quick Example

`curl -X 'GET' http://localhost:5000/api/classify -d '{"data": "May 14 05:47:20 switch-1.rm1.dal PortSec: %ETH-4-HOST_FLAPPING: Host ff:ff:ff:ff:ff:ff in VLAN 2600 is flapping between interface Port-Channel444 and interface Ethernet12 (message repeated 23 times in 5.51062 secs)"}' -H 'Content-Type: application/json'
`
```
{"results":[{"TIME":"May 14 05:47:20"},{"DEVICE":"switch-1.rm1.dal"},{"FACILITY":"ETH-4-HOST_FLAPPING"},{"VLAN":"VLAN 2600"},{"ACTION":"flapping"},{"INTERFACE":"Channel444"},{"INTERFACE":"Ethernet12"}]}
```

# Why NER?

We began exploring more automated ways of extracting important information from network device logs after building multiple services around them to provide troubleshooting information to network engineers. The regex extractions became a small nightmare to maintain for every device type and message format, especially for devices that did not log in a structured log format. At the same time, we were also exploring creating log vectors for similarity comparisons and building knowledge graphs, which would require entity extraction. Once we saw the power and performance of spaCy's NER pipeline using CNNs, we quickly realized this could free us from regex hell for most of our engineering needs and would be easier to read and maintain in the long run with the ability to quickly train and test offline. 

We hope to continue to explore this path of using NLP against structured logs and see just how deep the rabbit hole goes!

# Getting Started

Lets get started on entity extraction!

## Install requirements
- Setup a Python3 virtualenv
`python3 -m venv /path/to/new/virtual/environment`
- Activate the env to install requirements
`source /path/to/new/virtual/environment/bin/activate`
- Install requirements
`pip3 install -r requirements.txt`

## Train Model

Dolabra ships with a very basic NER model pre-trained on Cisco/Arista log format but it is trivial to add to or change the training data and retrain. 

In `utilities/` you will find a file `syslog1.yaml`. This is the format your training logs need to be in. 
 1. The raw log
 2. list of entities, their corresponding character positions in the raw log and the label for the entity

```
---
training_set:
  - training_log:
      log: "May 14 05:47:19 tor01.ra1.dal Ebra: %LINEPROTO-5-UPDOWN:Line protocol on Interface Ethernet28 (UPLINK) changed state to up"
      entities:
        - {start: 0, end: 15, label: "TIME"}
        - {start: 16, end: 29, label: "DEVICE"}
        - {start: 37, end: 55, label: "FACILITY"}
        - {start: 84, end: 94, label: "INTERFACE"}
        - {start: 96, end: 122, label: "INTERFACE-DESCRIPTION"}
        - {start: 123, end: 130, label: "ACTION"}
        - {start: 140, end: 142, label: "STATE"}
```
**Note*** We are aware that this is a painful process and the next release will contain a web based gui for labeling and training via Prodigy!

Once the training data has been finished, use the `model_train.py` script to train the data.
`python model_train.py`

## Running the Application
The default will use gunicorn as the WSGI server but you can use which ever you prefer. The command below also uses a single worker on a single thread, tune as needed. 

*Ideally, for production, you should have a proxy such as nginx, in front so as not to overwhelm gunicorn. 

Lets get it running!
`gunicorn -b 0.0.0.0:5000 app:app --reload`

This will launch the application listening on port 5000 (change as needed) and is now ready for entity extraction from logs submitted to it! 

*Note on performance*
The API has been stress tested with `wrk` and a LUA script to submit real logs to classify directly against the gunicorn service (not ideal, use nginx or other proxying services) in a container on a macbook pro ( quad-core i7 / 16GB RAM ) and was able to handle around 900 requests/s. 

## The API
You will need to submit logs in json format using the HTTP action 'GET' to the following endpoint: `/api/classify`

The payload format should be as follows:
```
{"data": "May 14 05:47:20 switch-1.rm1.dal PortSec: %ETH-4-HOST_FLAPPING: Host ff:ff:ff:ff:ff:ff in VLAN 2600 is flapping between interface Port-Channel444 and interface Ethernet12 (message repeated 23 times in 5.51062 secs)"}
```
Note: "data" is required as the entry key. 

# What's Coming
This is just the beginning for this project! The following are in the works!

 - A prebuilt container for those that just want to `docker run` and be off to the races
 - A GUI training/labeling interface that is much faster and easier than the yaml method
 - A more complete network device log model with more log/device types
 - Ability to interact with a message queue (kafka/nats/rabbit) for NER extraction
 - Better benchmarking stats
 - Unit tests!