#!/bin/bash

GR_LORA_DIR=/local/repository/gr_lora_sdr_powder

# Install prereqs
sudo apt-get -q update && \
    sudo apt-get -q -y install cmake swig liborc-0.4-dev || \
	{ echo "Failed to install prerequisites!"; exit 1; }

# Build and install LoRa GNU Radio modules
cd $GR_LORA_DIR && mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=`gnuradio-config-info --prefix` && \
    make && \
    sudo make install && \
    sudo ldconfig || \
	{ echo "Failed to build and install LoRa GNU Radio modules!"; exit 1; }
