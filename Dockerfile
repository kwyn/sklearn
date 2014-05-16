############################################################
# Dockerfile to build scikit-learn images
# Based on Ubuntu
############################################################

#Set base image to Ubuntu
FROM ubuntu

#File / Author Maintainer
MAINTAINER Kwyn Meagher

#Update repositor source list
RUN sudo apt-get update

################## BEGIN INSTALLATION ######################
#Install python basics
RUN apt-get -y install \
	build-essential \
	python-dev \
	python-setuptools \
	python-pip

#Install scikit-learn dependancies
RUN apt-get -y install \
	python-numpy \
	python-scipy \
	libatlas-dev \
	libatlas3-base

#Install Flask and flask-restful
RUN pip install Flask 
RUN pip install flask-restful

#Install scikit-learn
RUN apt-get -y install python-sklearn

################## END INSTALLATION ########################

#Add hello world script
ADD . /src/

#run hello world script
CMD "python" "/src/server.py"