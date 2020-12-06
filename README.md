# Deploy a ML model into Google Cloud Function using Serverless Framework

## Prerequisites
 - UNIX environment
 - Node.js (for npm)
 - Serverless 
 - Google Cloud Functions Provider Plugin
 - Google cloud console
 
## Steps 
refer this [link](https://www.serverless.com/framework/docs/providers/google/cli-reference/)

### 1. Create New Service
Create service in current working directory:

`serverless create --template google-pyhton`

Create service in new folder:

`serverless create --template google-pyhton --path my-function`

### 2. Setup Google Credentials (Provided you have a GCP Project setup with associated Billing account)

#### APIs
Go to the API dashboard, select your project and enable the following APIs (if not already enabled):

 - Cloud Functions API
 - Cloud Deployment Manager V2 API
 - Cloud Build API
 - Cloud Storage
 - Cloud Logging API
 
#### Credentials via Service account

 - Go to the Google Cloud Console.
 - Choose the project that you are working on from the top drop down
 - Click IAM & admin menu on left-sidebar
 - Then click Service accounts on left-sidebar
 - Click CREATE SERVICE ACCOUNT button on the top
 - Input Service account name and Service account ID will be generated automatically for you. Change it if you wish to.
 - Click Create button
 - Add Deployment Manager Editor, Storage Admin, Logging Admin, Cloud Functions Developer roles and click Continue
 - Click +CREATE KEY button and select JSON key type and click Create button
 - You will see a json (AKA keyfile) file downloaded
 - Click Done button
 - Save the keyfile somewhere secure. We recommend making a folder in your root folder and putting it there. Like this, ~/.gcloud/keyfile.json. You can change the file name from keyfile to anything. Remember the path you saved it to.
 
## 3. Update codes

Update the `main.py` to add main code for the service, `serverless.yml` should contain the configuration
Add `requirements.txt` if you need extra packages at runtime

## 4. Deploy
Deploy the function using 

`serverless deploy -v`


## Note
 - The Service created in this repo is for image classification using MobileNetV2 network on Imagenet dataset
 - the model and Labels were stored in a GCS Bucket check.
 - To allow unauthenticated invokation : Select the function, Show info panel, Click Add Member, Add the User `allUsers` and grant `Cloud Functions Invoker` and Save

