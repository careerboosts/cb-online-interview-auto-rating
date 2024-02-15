from bson import ObjectId
from fastapi.responses import JSONResponse
import logging
from pymongo import MongoClient
import os
import requests
import time
import json



cb_env = str(os.getenv('CB_ENVIRONMENT'))
client = MongoClient("mongodb://cb-mongo-svc-dev:K1BRCsPHJhxaJrdCbEjkdHyCaxhehYlFucNMzhUJYNcp5ybhHe3xvlYLt9YB5joankTWbTvxA7r9c1zpNYxbNw==@cb-mongo-svc-dev.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cb-mongo-svc-dev@")
database = client['smart-recruitement-dev']

Assessments_collection=database.get_collection('assessments')
Roles_collection = database.get_collection('roles')
Candidates_collection=database.get_collection('candidates')
Credentials_collection=database.get_collection('credentials')
Courses_collection=database.get_collection('courses')
Competencies_collection=database.get_collection('competencies')
Certifications_collection=database.get_collection('certifications')
Curriculums_collection=database.get_collection('curriculums')
Questions_collection = database.get_collection('frequentInterviewQuestions')
Employees_collection = database.get_collection('employees')
Feedbacks_collection=database.get_collection('feedbacks')
TailoredRole_collection = database.get_collection('TailoredRole')
Users_collection = database.get_collection('users')
Managers_collection = database.get_collection('managers')
Careerboosts_Collection = database.get_collection('careerboosts')
Participations_collection=database.get_collection('participations')
Package_collection=database.get_collection('packages')
Projects_collection = database.get_collection('projects')
Recruiters_collection = database.get_collection('recruiters')
Scores_collection = database.get_collection('scores')
Proctoring_collection = database.get_collection('proctoring')
CheatingAttempts_collection = database.get_collection('cheatingAttempts')
Recommandations_collection= database.get_collection('recommandations')
CurrentProfiles_collection = database.get_collection('currentProfiles')
TargetProfiles_collection = database.get_collection('targetProfiles')
Links_collection = database.get_collection('links')
Quotes_collection=database.get_collection('idpQuotes')
Schedule_collection=database.get_collection('schedule')
Subscription_collection=database.get_collection('subscriptions')
Organization_collection=database.get_collection('organizations')
Category_Questions_collection=database.get_collection('categoryQuestions')
Questions_collection=database.get_collection('Questions')
client_secret= os.getenv('CLIENT_SECRET')
client_id = os.getenv('CLIENT_ID')

# OIDC_TOKEN_URL = os.getenv("OIDC_TOKEN_URL")
# REGISTER_URL = os.getenv("REGISTER_URL")

# OIDC_TOKEN_URL = "http://keycloak.tools.svc.cluster.local/realms/master/protocol/openid-connect/token"
# REGISTER_URL = "http://keycloak.tools.svc.cluster.local/admin/realms/careerboosts/users"
OIDC_TOKEN_URL = "https://auth-b2c-dev.careerboosts.com/realms/master/protocol/openid-connect/token"
REGISTER_URL = "https://auth-b2c-dev.careerboosts.com/admin/realms/careerboosts/users"
# OIDC_TOKEN_URL = "https://auth-b2c.careerboosts.com/realms/master/protocol/openid-connect/token"
# REGISTER_URL = "https://auth-b2c.careerboosts.com/admin/realms/careerboosts/users"



# pearson functions
x_api_key =os.getenv('CLIENT_SECRET')
#  os.getenv("X_API_KEY")
pearson_url = "https://api.sandbox.eu.connect.talentlens.com"
username = "hamzaghenimi98@gmail.com"
password = "Pearson.11"

# get token
def authenticate(): 
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        # "x-api-key": x_api_key
    }
    payload = {
        "username": username,
        "password": password
    }

    try:
        r = requests.post(pearson_url + "/v1/authentication/token", headers=headers, data=payload, verify=False)
        return {"error": False, "status": r.status_code, "detail": r.json()["data"]["accessToken"]}
    except RuntimeError as error:
        return {"error": True, "status": 500, "detail": "Server error"}

# Get all products
def getProducts():
    data = authenticate() 
    if data["error"]: return {"error": True, "status": data.status, "detail": data["error"]}

    headers = {
        "Authorization": "Bearer " + data["detail"],
        # "x-api-key": x_api_key
    }

    try:
        r = requests.get(pearson_url + "/v1/products", headers=headers)
        return {"error": r.status_code > 200, "status": r.status_code, "detail": r.json()}
    except RuntimeError as error:
        return {"error": True, "status": 500, "detail": "Server error"}

# get one product
def getProduct(id):
    data = authenticate() 
    if data["error"]: return {"error": True, "status": data.status, "detail": data["error"]}

    headers = {
        "Authorization": "Bearer " + data["detail"],
        # "x-api-key": x_api_key
    }

    try:
        r = requests.get(pearson_url + "/v1/products/" + id, headers=headers)
        return {"error": r.status_code > 200, "status": r.status_code, "detail": r.json()}
    except RuntimeError as error:
        return {"error": True, "status": 500, "detail": "Server error"}

# Create new schedule
def createSchedule(payload):
    data = authenticate() 
    if data["error"]: return {"error": True, "status": data.status, "detail": data["error"]}

    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + data["detail"],
        # "x-api-key": x_api_key
    }

    try:
        r = requests.post(pearson_url + "/v1/schedules", headers=headers, data=json.dumps(payload))
        return {"error": r.status_code > 201, "status": r.status_code, "detail": r.json()}
    except RuntimeError as error:
        print(error)
        return {"error": True, "status": 500, "detail": "Server error"}   
    
def getScheduleStatus(id):
    data = authenticate() 
    if data["error"]: return {"error": True, "status": data.status, "detail": data["error"]}

    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + data["detail"],
        # "x-api-key": x_api_key
    }

    try:
        r = requests.get(pearson_url + "/v1/schedules/" + id, headers=headers)
        return {"error": r.status_code > 200, "status": r.status_code, "detail": r.json()}
    except RuntimeError as error:
        return {"error": True, "status": 500, "detail": "Server error"} 
    
def getResult(scheduleId, customerId=None):
    data = authenticate() 
    if data["error"]: return {"error": True, "status": data.status, "detail": data["error"]}

    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + data["detail"],
        # "x-api-key": x_api_key
    }

    try:
        if customerId:
            r = requests.get(pearson_url + "/v1/results/" + scheduleId + "?candidateId=" + customerId, headers=headers)
            return {"error": r.status_code > 200, "status": r.status_code, "detail": r.json()} 
        else:
            r = requests.get(pearson_url + "/v1/results/" + scheduleId, headers=headers)
            return {"error": r.status_code > 200, "status": r.status_code, "detail": r.json()} 
    except RuntimeError as error:
        return {"error": True, "status": 500, "detail": "Server error"} 

# create new schedule and save it in the database
def saveSchedule(projectId, employeeId, groupId):
  project_doc = Projects_collection.find_one({"_id": ObjectId(projectId)})
  employee_doc = Employees_collection.find_one({"_id": employeeId})
  groups = project_doc["projectGroups"]
  productsIds = []

  for group in groups:
    if group["group_id"] == groupId: 
      curriculumId = group["groupCurriculums"][0]
      curriculum_doc = Curriculums_collection.find_one({"_id": ObjectId(curriculumId)})
      for assessment in curriculum_doc["curriculumAssessments"]:
        if (isItPearsonAssessmentId(assessment)):   # check if there is any pearson assessment
          productsIds.append(str(getAssessmentProductId(assessment)))
  
  user_doc = Users_collection.find_one({"_id": ObjectId(employee_doc["employeeUserId"])})
  user = {
            "candidateId": str(user_doc["_id"]),
            "firstName": user_doc["userFirstName"], 
            "lastName": user_doc["userLastName"], 
            "email": user_doc["userEmail"]
          }
  if (len(productsIds)):
    payload = {
      "products": [
            {
              "productId": productId,
              "languageCode": "en-US",
              "canOverrideLanguage": True
            } for productId in productsIds
      ],
      "candidates": [
          {
            "candidateId": user["candidateId"],
            "tags": [ # voluntary fields
              {
                "key": "email",
                "value": user["email"]
              },
              {
                "key": "GivenName",
                "value": len(user["firstName"]) and user["firstName"] or "Unknown"
              },
              {
                "key": "FamilyName",
                "value": len(user["lastName"]) and user["lastName"] or "Unknown"
              }
            ]
          }
        ]
    }
    data = createSchedule(payload)
    # for assessmentId in 
    scheduleId = data["detail"]["data"]["scheduleId"]
    scheduleUrl = data["detail"]["data"]["urls"][0]["url"]
    for assessmentId in productsIds:
      Schedule_collection.insert_one({
        "scheduleId": scheduleId,
        "scheduleUrl": scheduleUrl,
        "scheduleProjectId": projectId,
        "scheduleAssessmentId": assessmentId,
        "scheduleUserId": ObjectId(user_doc["_id"])
      })
        

def isItPearsonAssessmentId(assessmentId):
  assessment_doc = Assessments_collection.find_one({"_id": ObjectId(assessmentId)})
  if assessment_doc["assessmentProvider"].lower() == "pearson":
    return True
  return False

def getAssessmentProductId(assessmentId): 
  assessment_doc = Assessments_collection.find_one({"_id": ObjectId(assessmentId)})
  return assessment_doc["assessmentId"]

# script to update pearson assessments
def updateAssessments():
    assessments = getProducts()
    for assessment in assessments["detail"]:
        # check if assessment already exists in the database
        if Assessments_collection.find_one({"assessmentId": assessment["productId"]}):
            continue  # skip this assessment and move on to the next one
        # otherwise, add the assessment to the database
        new_assessment = {
            "assessmentId": assessment["productId"],
            "assessmentName": assessment["title"],
            "assessmentType": "external",
            "assessmentProvider": "Pearson"
        }
        Assessments_collection.insert_one(new_assessment)
   
    
# keycloack functions
def getToken():
  access_token = None

  payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
  }

  try:
    r = requests.post(OIDC_TOKEN_URL, data=payload)
    if (r.status_code > 200):
       return {"error": True, "status": 404, "detail": "Invalid OIDC_TOKEN_URL!"}
    access_token = r.json()["access_token"]
    return {"error": False, "status": 200, "detail": access_token}
  except requests.exceptions.HTTPError:
    return {"error": True, "status": 400, "detail": "Http Error!"};
  except requests.exceptions.ConnectionError: 
    return {"error": True, "status": 503, "detail": "Error Connecting!"};
  except requests.exceptions.Timeout: 
    return {"error": True, "status": 408, "detail": "Timeout Error!"};
  except requests.exceptions.RequestException: 
    return {"error": True, "status": 500, "detail": "Unexpected error!"}


def createUser(user):
    res = getToken()
    if (res["error"]): return res
    headers  = {
      "Content-Type": "application/json", 
      "Authorization": "Bearer " + res["detail"] 
     }
    rslt = None
    try:
      r = requests.post(REGISTER_URL, headers=headers, data=json.dumps(user))
      # Status code 401 Invalid token 
      # Status code 409 == user already exists 
      # Satus code 201 == new user created
      return {
         "error": r.status_code > 201, 
         "status": r.status_code,
         "detail": "Invalid token!" 
                    if r.status_code == 401 
                    else "user already exists!" 
                    if r.status_code == 409 
                    else "Invalid REGISTER_URL!"
                    if r.status_code == 404
                    else "user registred successfully"
      }
    except RuntimeError as error:
      return {"error": True, "status": 500, "detail": "Unexpected error: " + error}
    
def createUsers(usersList):
  access_token = getToken()
  if (access_token):
    headers  = {
      "Content-Type": "application/json", 
      "Authorization": "Bearer " + access_token 
    }
    ptr = 0
    rslt = None
    for user in usersList:
      if ptr == 5:
        time.sleep(5)
        ptr = 0
      try:
        r = requests.post(REGISTER_URL, headers=headers, data=json.dumps(user))
        # status code 401 Invalid token /status code 409 == user already exists / satus code 201 == new user created
        rslt = r.status_code
      except RuntimeError as error:
        rslt = error
      finally:
        ptr += 1
    return rslt
  else: 
    return "No access token!"

async def get_project_informations(project_id):
    project = await Projects_collection.find_one({"projectId": project_id})
    return project
    


async def get_participation_progress(user_id):
    try:
        participation = await Participations_collection.find_one({"participationUserId": user_id})
        return participation.get('participationStatus')
    except Exception as e:
        logging.error("Participation not found for {}: Exception: {}".format(user_id, e))


