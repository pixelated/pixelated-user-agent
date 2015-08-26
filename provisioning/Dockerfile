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


FROM debian:jessie

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
    apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3 && \
    apt-key adv --keyserver pool.sks-keyservers.net --recv-key 837C1AD5367429D9

RUN echo "Package: python-sqlcipher" > /etc/apt/preferences.d/python-sqlcipher
RUN echo "Pin: version 2.6.3.3+0~20141111222659.14+wheezy~1.gbp2d164a+pix1" >> /etc/apt/preferences.d/python-sqlcipher
RUN echo "Pin-Priority: 1000" >> /etc/apt/preferences.d/python-sqlcipher

# Update packages lists
RUN apt-get update -y --force-yes

# Set the locale
# Install program to configure locales
RUN apt-get install -y locales
RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales && \
  locale-gen C.UTF-8 && \
  /usr/sbin/update-locale LANG=C.UTF-8
# Install needed default locale for Makefly
RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && \
  locale-gen
# Set default locale for the environment
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install pip for taskthread dependency (no backport yet)
RUN apt-get install python-pip python-all-dev libssl-dev
RUN pip install taskthread

RUN apt-get install -y --force-yes --allow-unauthenticated soledad-client soledad-common
# Install Pixelated User Agent
RUN apt-get install -y --force-yes pixelated-user-agent

EXPOSE 4567
