from django.shortcuts import render

# Create your views here.
from .models import Issue, Reporter, CriticalIssue, LowPriorityIssue

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

 
 
REPORTERS_FILE = "reporters.json"
ISSUES_FILE = "issues.json"
 
 
def read_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
 
 
def write_file(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
 
 

 
@csrf_exempt  
def reporters(request):
 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
 
            reporter = Reporter(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                team=data["team"]
            )
 
            reporter.validate()
 
            reporters_list = read_file(REPORTERS_FILE)
            reporters_list.append(reporter.to_dict())
            write_file(REPORTERS_FILE, reporters_list)
 
            return JsonResponse(reporter.to_dict(), status=201)
 
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
 
    
    elif request.method == "GET":
 
        
        reporter_id = request.GET.get("id")
 
        reporters_list = read_file(REPORTERS_FILE)
 
        if reporter_id:
            # Loop through the list and find the matching reporter
            for reporter in reporters_list:
                if reporter["id"] == int(reporter_id):
                    return JsonResponse(reporter, status=200)
 
            # Nothing matched — return 404
            return JsonResponse({"error": "Reporter not found"}, status=404)
 
        else:
            # No ID given — return everyone
            # safe=False allows us to return a list instead of a dict
            return JsonResponse(reporters_list, safe=False, status=200)
 
 
 
@csrf_exempt
def issues(request):
 
    # ── POST /api/issues/ — Create a new issue ──
    if request.method == "POST":
        try:
            # Step 1 — Read the JSON body
            data = json.loads(request.body)
 
           
            priority = data["priority"]
 
            if priority == "critical":
                issue = CriticalIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"]
                )
            elif priority == "low":
                issue = LowPriorityIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"]
                )
            else:
                # medium or high — use the base Issue class
                issue = Issue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"]
                )
 
            # Step 3 — Validate
            issue.validate()
 
            response_data = issue.to_dict()
            response_data["message"] = issue.describe()
 
            # Step 5 — Save to issues.json
            issues_list = read_file(ISSUES_FILE)
            issues_list.append(issue.to_dict())  # save without message key
            write_file(ISSUES_FILE, issues_list)
 
            # Step 6 — Return response with 201 status
            return JsonResponse(response_data, status=201)
 
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
 
    # ── GET /api/issues/ — Get all issues, one by ID, or filtered by status ──
    elif request.method == "GET":
 
        issue_id = request.GET.get("id")
        status_filter = request.GET.get("status")
 
        issues_list = read_file(ISSUES_FILE)
 
        # Filter by ID
        if issue_id:
            for issue in issues_list:
                if issue["id"] == int(issue_id):
                    return JsonResponse(issue, status=200)
            return JsonResponse({"error": "Issue not found"}, status=404)
 
        # Filter by status
        elif status_filter:
            filtered = [i for i in issues_list if i["status"] == status_filter]
            return JsonResponse(filtered, safe=False, status=200)
 
        # Return all issues
        else:
            return JsonResponse(issues_list, safe=False, status=200)