# DOCKER-VERSION 1.1.0
#
# Copyright (c) 2014 ThoughtWorks Deutschland GmbH
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

# builds the pixelated-user-agent using the debian packages

FROM debian:testing

MAINTAINER fbernitt@thoughtworks.com

# Force -y for apt-get
RUN echo "APT::Get::Assume-Yes true;" >>/etc/apt/apt.conf

# Install Pixelated User Packages
RUN echo "deb http://packages.pixelated-project.org/debian wheezy-snapshots main" >> /etc/apt/sources.list
RUN echo "deb http://packages.pixelated-project.org/debian wheezy-backports main" >> /etc/apt/sources.list
RUN echo "deb http://packages.pixelated-project.org/debian wheezy main" >> /etc/apt/sources.list
RUN echo "deb http://deb.bitmask.net/debian/ wheezy main" >> /etc/apt/sources.list
RUN echo "deb http://deb.leap.se/experimental wheezy main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver pool.sks-keyservers.net --recv-key 1E34A1828E207901 && \
    apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

# Update packages lists
RUN apt-get update -y --force-yes

# Install pip for taskthread dependency (no backport yet)
RUN apt-get install python-pip
RUN pip install taskthread

RUN apt-get install -y --force-yes --allow-unauthenticated soledad-client=0.6.1~509f76c soledad-common=0.6.1~509f76c
# Install Pixelated User Agent
RUN apt-get install -y --force-yes pixelated-user-agent

EXPOSE 4567

