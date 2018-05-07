# Azure IoT Edge "Scott or Not" Sample

This is a code sample for an IoT Edge solution that takes images from a camera feed on an edge device, runs them through a custom vision module, and pushes the results to an Azure Function on the device to take an action.  The model included with the sample will classify images containing Scott Guthrie.  You can easily [replace the model with any Custom Vision Service model](#changing-the-model)

## Setup

### Pre-reqs

* Visual Studio Code
    * Docker Extension
    * Azure IoT Hub Extension
* Docker
* Python 2.7
* `iotedgectl` installed on devices ([Windows](https://docs.microsoft.com/azure/iot-edge/quickstart) or [Linux/Raspberry Pi](https://docs.microsoft.com/azure/iot-edge/quickstart-linux))
* Azure Subscription (free trial is fine)
* Azure IoT Hub

If you plan to run on a Raspberry Pi, it's recommended to use a Raspberry Pi 3 with a `picamera` enabled camera and a SenseHat running linux.

If you plan to run on a Windows PC, be sure to [read the following](#running-the-solution-on-a-windows-machine)

### Configuration

* Clone the repository and open it in Visual Studio Code
* Open the **Azure IoT Hub Devices** extension and connect to an IoT Hub in Azure
* Configure the docker registry you want to publish the container images. [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal) is a great choice.  Update the `[registry]` placeholder in the three `module.json` files with the registry you have authorization to use.

There are two templates included with the samples located in the `templates/` directory.  Depending on where you are planning to build and deploy (Windows or Linux Raspberry Pi), copy the `deployment.template.json` file to the base of the project.  This will enable you to right-click the template and **Build the IoT Edge Solution**

To build the solution, copy a `deployment.template.json` file to the base of the project, right-click the file, and select **Build the IoT Edge Solution**.  This will build the docker images and publish them to your docker registry.  It will also generate a `config/deployment.json` file you can use to deploy to an edge device.

Right-click the `config/deployment.json` file to **Create Deployment for IoT Edge Device**.  This will allow you to select the IoT Edge device running `iotedgectl` to deploy the solution.  

Be sure to note in the `deployment.template.json` file and the generated `deployment.json` file is an environment variable for the AzureFunctionContainer that contains the URL for the Logic App to call to post a tweet.  This should be replaced with the URL of your own Logic App that has an HTTP Request trigger.

## Running the solution on a Windows machine

Currently Docker for Windows doesn't allow sharing devices from the host operating system with containers, even when using the `--privileged` flag.  The issue [is being tracked here](https://github.com/docker/for-win/issues/1018) and should be resolved in an upcoming release.  In the meantime the Windows deployment template includes an environment variable that will pull the image from `C:\Image\picture.jpg` instead of the webcam.  If you want to automatically generate `picture.jpg` files in real-time from the webcam you can use [this simple console application](https://github.com/jeffhollan/csharp-camera-capture-to-image/releases/tag/0.1) which will take the camera feed and save `picture.jpg` files.  Extract all of the files in a directory and then run the `.exe` file.

Also be sure to share the C drive with Docker using the Docker for Windows settings.

## Personalizing the sample

### Changing the model

You can replace the model in this sample with a different TensorFlow model.  The [Azure Custom Vision](https://customvision.ai/) allows you to easily create and train models using sample images.  After training an image set, select **Export** and choose **Android / TensorFlow**.  Rename `labels.txt` to `model.pbtxt` and replace the `model.pb` and `model.pbtxt` files in the CustomVisionContainer with the generated entities.  You'll also likely want to change the code in the `run.csx` file for the AzureFunctionContainer to not be looking for the tags `Scott` and `NotScott`.  

Rebuild and deploy your solution (⚠ don't forget to increment the version in the `module.json` file) to have solution leverage your own custom model.

