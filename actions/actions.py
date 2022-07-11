# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
from dis import dis
import ldap

#
# def authenticate(address, username, password):
#     conn = ldap.initialize('ldap://' + address)
#     conn.protocol_version = 3
#     conn.set_option(ldap.OPT_REFERRALS, 0)
#     return conn.simple_bind_s(username, password)


# authenticate("172.16.19.20", "CN=Administrator,CN=Users,DC=tcplcoe,DC=com", "Xanadu@@12345")

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import UserUtteranceReverted, ActionReverted
from rasa_sdk.events import Restarted
import webbrowser
from time import sleep
import json

from typing import Any, Text, Dict, List
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Text
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.channels import BotFrameworkInput
import requests
import rasa.core.lock_store

logger = logging.getLogger(__name__)
from rasa_sdk.forms import FormAction

# class ActionGreetUser(Action):
#
#     def name(self) -> Text:
#         return "action_greet_user"
#
#     @classmethod
#     def authenticate(cls, address, username, password):
#         conn = ldap.initialize('ldap://' + address)
#         print(conn.fileno())
#         conn.protocol_version = 3
#         conn.set_option(ldap.OPT_REFERRALS, 0)
#         return conn.simple_bind_s(username, password)
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         Restarted()
#         username = "kuldeep"
#         try:
#             user_information_str = tracker.sender_id
#             user_information_str_dict = eval(user_information_str)
#             username = user_information_str_dict.get("name")
#             email = user_information_str_dict.get("email")
#             user_id = user_information_str_dict.get("id")
#             logger.debug(user_id)
#             logger.debug(email)
#             logger.debug(username)
#         except Exception as e:
#             print(e)
#         username = tracker.get_slot("username")
#         password = tracker.get_slot("password")
#         try:
#             ActionGreetUser.authenticate("172.16.19.20", "CN=Administrator,CN=Users,DC=tcplcoe,DC=com", "Xanadu@@12345")
#
#             dispatcher.utter_message(
#                 f"Hey {username} 👋\nI am your  assitant, what may I help you with today ?")
#             # for uncomment the code for team and same code pattern in doamin.yaml for buttons
#             # buttons = [{"type": "imBack", "title": "Printer spooler", "value": "/printerIssue"},
#             #            {"type": "imBack", "title": "Make Chrome Default", "value": "/chromeDefault"},
#             #            {"type": "imBack", "title": "Slow Machine", "value": "/slowMachine"}]
#             buttons = [{"title": "Printer spooler", "payload": "/printerIssue"},
#                        {"title": "Make Chrome Default", "payload": "/chromeDefault"},
#                        {"title": "Slow Machine", "payload": "/slowMachine"}]
#             dispatcher.utter_button_message("Button", buttons)
#         except:
#             dispatcher.utter_message("You are not authenticate")
#         return [UserUtteranceReverted()]
#

"""
Generic ticket create function
"""


class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # custom behavior
        return [Restarted()]


class ActionMainMenu(Action):

    def name(self) -> Text:
        return "action_main_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            logger.info(e)
        buttons = [{"title": "SYSTEM", "payload": "/system"},
         {"title": "MICROSOFT OFFICE", "payload": "/microsoftOffice"},
         {"title": "BROWSER", "payload": "/Browser"},
         {"title": "CONNECTIVITY", "payload": "/connectivity"},
         {"title": "SOFTWARE", "payload": "/software"},
         {"title": "OUTLOOK", "payload": "/outlook"},
         {"title": "AD SELF SERVICE", "payload": "/AdSelfService"},
         {"title": "SOFTWARE INSTALLATION", "payload": "/software"},
         {"title": "REMOTE SUPPORT", "payload": "/remoteSupport"},
         {"title": "PRINTER", "payload": "/Printer"}
         ]
        dispatcher.utter_button_message("", buttons)
        return [UserUtteranceReverted()]


def generate_rimcc_ticket(subject):
    url = "https://rimccsupport.teamcomputers.com/sdpapi/request/"

    inputdata = {
        "operation": {
            "details": {
                "requester": "Guest",
                # currently requester is "Guest" bydefault till the user authentication is being done.
                "subject": subject,
                "requesttemplate": "Default Request",
                "site": "Gurgaon",
                "account": "Asahi India Glass"
            }
        }
    }
    payload = {"INPUT_DATA": json.dumps(inputdata), "OPERATION_NAME": "ADD_REQUEST",
               "TECHNICIAN_KEY": "5900ADE4-B52C-4556-AE62-B2CDCD2402B7", "format": "json"}
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload)
    if response.json()['operation']['result']['status'] == 'Success':
        return response
    else:
        return None


class ActionCategoryOfIssues(Action):

    def name(self) -> Text:
        return "action_category_of_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            logger.info(e)
        dispatcher.utter_message("Hello, I am AIS TechMate, I'm AI powered assistant. I am here to help you with your queries. Please select a topic relevant to your query from the list below to proceed.")

        buttons = [{"title": "SYSTEM", "payload": "/system"},
                   {"title": "MICROSOFT OFFICE", "payload": "/microsoftOffice"},
                   {"title": "BROWSER", "payload": "/Browser"},
                   {"title": "CONNECTIVITY", "payload": "/connectivity"},
                   {"title": "SOFTWARE", "payload": "/software"},
                   {"title": "OUTLOOK", "payload": "/outlook"},
                   {"title": "AD SELF SERVICE", "payload": "/AdSelfService"},
                   {"title": "SOFTWARE INSTALLATION", "payload": "/software"},
                   {"title": "REMOTE SUPPORT", "payload": "/remoteSupport"},
                   {"title": "PRINTER", "payload": "/Printer"}
                   ]
        dispatcher.utter_button_message("", buttons)

        return [UserUtteranceReverted()]




class ActionSubCategoryOfSystemIssues(Action):

    def name(self) -> Text:
        return "action_subcategory_of_system_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Speed up machine", "payload": "/speedUpMachine"},
                   #    {"title": "Oracle Not Working ", "payload": "/oracleNotWorking"},
                   {"title": "Set time Zone to india standard time", "payload": "/setTimeZoneToIndiaStandardTime"},
                   {"title": "Resolve blue dump error", "payload": "/resolveBlueDumpError"},
                   # {"title": "Enable JAVA auto update", "payload": "/EnableJAVAAutoUpdate"},
                   {"title": "Disable JAVA auto update", "payload": "/javaupdate"},
                   {"title": "Window issue due to update", "payload": "/windowIssueDueToUpdate"},
                   {"title": "Remote desktop connection troubleshooter",
                    "payload": "/remoteDesktopConnectionTroubleShooter"},
                   {"title": "Back up user data", "payload": "/backUpUserData"},
                   {"title": "Free up disk space", "payload": "/freeUpDiskSpace"},
                   {"title": "Update Group Policy", "payload": "/updateGroupPolicy"},
                   {"title": "Shared Folder for mapping", "payload": "/sharedFolderForMapping"},
                   {"title": "Restart critical services related to Anti-Virus",
                    "payload": "/antiVirusIsNotWorking"},
                   {"title": "Unable to open .JPG & .PNG files in Windows 10", "payload": "/unableToOpenFile"},

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfOutlookIssues(Action):

    def name(self) -> Text:
        return "action_subcategory_of_outlook_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Outlook is not connecting", "payload": "/outlookIsNotConnecting"},
                   {"title": "Create a new PST (Archive) File", "payload": "/createNewPSTArchiveFile"},
                   {"title": "Configure Outlook", "payload": "/configureOutlook"},
                   {"title": "Know your PST file size",
                    "payload": "/knowYourPSTFileSize"},
                   {"title": "Open Webmail",
                    "payload": "/openWebmail"},

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfBrowser(Action):

    def name(self) -> Text:
        return "action_subcategory_of_browser_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Unable to open PDF in IE", "payload": "/unableToOpenPDFInIE"},
                   {"title": "Make Chrome your default browser", "payload": "/makeChromeYourDefaultBrowser"},
                   {"title": "Set Internet Explorer as default browser",
                    "payload": "/setInternetExplorerDefaultBrowser"},
                   {"title": "Make Edge your default browser",
                    "payload": "/makeEdgeYourDefaultBrowser"},
                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfConnectivity(Action):

    def name(self) -> Text:
        return "action_subcategory_of_connectivity_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Lan not working", "payload": "/lanNotWorking"},
                   {"title": "Unable to connect to Wi-Fi", "payload": "/unableToConnectToWi-Fi"},
                   {"title": "Modify the hosts file on your machine",
                    "payload": "/modifyTheHostsFileOnYourMachine"},
                   {"title": "Internet/ LAN limited issue",
                    "payload": "/internetLANLimitedIssue"},
                   {"title": "Check Internet working or not", "payload": "/checkInternetWorkingOrNot"},
                   {"title": "Check internet quality and speed", "payload": "/checkInternetQualityAndSpeed"},
                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfPrinter(Action):

    def name(self) -> Text:
        return "action_subcategory_of_printer_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Getting error Printer Spooler Service is not running",
                    "payload": "/printerSpoolerServiceIsNotRunning"},

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfAdService(Action):

    def name(self) -> Text:
        return "action_subcategory_of_ad_service_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Reset your password from anywhere",
                    "payload": "/resetYourPasswordFromAnywhere"},
                   {"title": "Enroll in ADSelfService Plus portal",
                    "payload": "/enrollInADSelfServicePlusPortal"},

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfSoftwareInstall(Action):

    def name(self) -> Text:
        return "action_subcategory_of_software_install_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Cisco Webex Meetings Installation",
                    "payload": "/ciscoWebexMeetingsInstallation"},
                   {"title": "Google chrome Installation",
                    "payload": "/googleChromeInstallation"},
                   {"title": "Adobe Reader Installation",
                    "payload": "/adobeReaderInstallation"},
                   {"title": "WinRAR Installation",
                    "payload": "/winRARInstallation"},

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfRemoteSupport(Action):

    def name(self) -> Text:
        return "action_subcategory_of_remote_support_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Join Remote Support Session",
                    "payload": "/joinRemoteSupportSession"},
                   {"title": "Install Remote Support software",
                    "payload": "/installRemoteSupportSoftware"},

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionSubCategoryOfMicrosoftIssues(Action):

    def name(self) -> Text:
        return "action_subcategory_of_microsoft_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Restarted()
        try:
            user_name = tracker.sender_id
            logger.debug(user_name)
        except Exception as e:
            raise e
        dispatcher.utter_message(
            f"Please choose from the given option")
        buttons = [{"title": "Speed up Microsoft Powerpoint", "payload": "/speedUpMicrosoftPowerpoint"},
                   {"title": "Office Quick Repair", "payload": "/officeQuickRepair"},
                   {"title": "Excel files not opening",
                    "payload": "/excelFilesNotOpening"},
                   {"title": "Excel random crash issues",
                    "payload": "/excelRandomCrashIssues"},
                   {"title": "Convert word file into pdf file",
                    "payload": "/convertWordFileIntoPdfFile"},
                   {"title": "Open Excel in safe mode", "payload": "/openExcelInSafeMode"}

                   ]
        dispatcher.utter_button_message("", buttons)

        # return [UserUtteranceReverted()]


class ActionCreateTicketForSpeedUpMachine(Action):

    def name(self) -> Text:
        return "action_ticket_creation_speed_up_ticket_creation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration

        subject = "Machine speed up."
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]

        print(
            "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
            "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionOpenLMS(Action):

    def name(self) -> Text:
        return "action_open_LMS"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sleep(3)
        webbrowser.open("http://teamworksnew.teamcomputers.com/SitePages/LeaveRequest.aspx")

        # return [UserUtteranceReverted()]


class ActionChromeSlowness(Action):

    def name(self) -> Text:
        return "action_chrome_slowness"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sleep(3)
        webbrowser.open("C:\Windows\IAssist\custom_scripts\663\deletechromebrowsinghistory.bat")
        return [UserUtteranceReverted()]


class ActionCreateTicketChromeSlowness(Action):

    def name(self) -> Text:
        return "action_ticket_creation_chromeSlowness"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration

        subject = "Chrome is slow"
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]

        print(
            "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
            "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketSlowExcel(Action):

    def name(self) -> Text:
        return "action_ticket_creation_slowExcel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "MS EXCEL slowness"
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        print(
            "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
            "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketPrinterIssue(Action):

    def name(self) -> Text:
        return "action_ticket_creation_printerIssue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration

        subject = "Printer issue"
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            logger.debug("dfdjgfjhdgfhegfjsfbjsgfhgsdfhgdsbgdcwghrfwghdfashdfwh")
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        print(
            "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
            "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketChromeDefault(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_chromeDefault"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Make Chrome Default"
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            logger.debug("dfdjgfjhdgfhegfjsfbjsgfhgsdfhgdsbgdcwghrfwghdfashdfwh")
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
            print(
                "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
                "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketDiskCleanup(Action):

    def name(self) -> Text:
        return "action_ticket_creation_diskCleanup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Need Disk Cleanup to be done on my system"
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc

        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]

        print(
            "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
            "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketSlowMachine(Action):

    def name(self) -> Text:
        return "action_ticket_creation_slowMachine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Machine gets slow."
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc

        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]

        print(
            "The following ticket has been created for you:-<br><br>Ticket Number:{}<br>Priority:{}<br>Subject:{}<br>Impact:{"
            "}<br>SLA:{}".format(ticket_number, priority, subject, impact, sla))

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # tk = '"<a href="https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID=44107">"{}"</a>"'.format(ticket_number,ticket_number)
        # print(tk)
        # dispatcher.utter_message(tk)

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# def create_ticket(username, password, description, title, category_id, category_name, sub_category_id,
#                   sub_category_name):
#     import requests
#     from requests import Session
#     from requests.auth import HTTPBasicAuth
#     from zeep import Client
#     from zeep.transports import Transport
#
#     session = Session()
#     session.verify = False
#     transport = Transport(session=session)
#
#     session.auth = HTTPBasicAuth(username, password)
#
#     client = Client('https://helpdeskim.dalmiabharat.com/ITSMWS/SapphireSD?wsdl', transport=Transport(session=session))
#
#     key = client.service.getAuthKey(client.service.Encode('fms_imsupport'),
#                                     client.service.Encode('Dalmia@12345').encode(),
#                                     "ims")
#
#     url = "https://helpdeskim.dalmiabharat.com/ITSMWS/SapphireSD?wsdl"
#     payload = "<Envelope xmlns=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n    <Body>\r\n        <createRequest xmlns=\"http://servicedesk.sims.tkd.com/\">\r\n            <!-- Optional -->\r\n            <request xmlns=\"\">\r\n                <additionalCCMailID></additionalCCMailID>\r\n                <additionalContactNumbers></additionalContactNumbers>\r\n                <additionalParams></additionalParams>\r\n                <approvalManagerName>--</approvalManagerName>\r\n                <assetID>0</assetID>\r\n                <CI></CI>\r\n                <categoryID>{category_id}</categoryID>\r\n                <categoryName>{category_name}</categoryName>\r\n                <creationTime>2020-08-04 11:46:51.0</creationTime>\r\n                <currentStateName>Assign</currentStateName>\r\n                <departmentID>1566</departmentID>\r\n                <departmentName>CEM Information Management</departmentName>\r\n                <derivedField1ID>207</derivedField1ID>\r\n                <derivedField1Name>NA</derivedField1Name>\r\n                <derivedField2ID>208</derivedField2ID>\r\n                <derivedField2Name>NA</derivedField2Name>\r\n                <derivedField3ID>306</derivedField3ID>\r\n                <derivedField3Name>DBL / DCBL HO</derivedField3Name>\r\n                <description>{description}</description>\r\n                <errorMessage></errorMessage>\r\n                <expectedClosureTime></expectedClosureTime>\r\n                <impactID>0</impactID>\r\n                <impactName></impactName>\r\n                <locationID>44</locationID>\r\n                <locationName>Noida</locationName>\r\n                <owner>FMS IM Support</owner>\r\n                <priorityID>0</priorityID>\r\n                <priorityName></priorityName>\r\n                <problemID>384089</problemID>\r\n                <projectID>7</projectID>\r\n                <projectName>Service Request</projectName>\r\n                <recordTypeID>10</recordTypeID>\r\n                <requestType>Service Request</requestType>\r\n                <serviceID>317</serviceID>\r\n                <serviceName>User Services</serviceName>\r\n                <sourceID>0</sourceID>\r\n                <sourceName>Web</sourceName>\r\n                <stateID>173</stateID>\r\n                <subCategoryID>{sub_category_id}</subCategoryID>\r\n                <subcategoryName>{sub_category_name}</subcategoryName>\r\n                <submiitedBy>FMS IM Support</submiitedBy>\r\n                <submitter>2271</submitter>\r\n                <title>{title}</title>\r\n                <urgencyID>0</urgencyID>\r\n                <urgencyName></urgencyName>\r\n                <workGroupID>31</workGroupID>\r\n                <workgroupName>Server Group</workgroupName>\r\n            </request>\r\n            <authKey xmlns=\"\">{key}</authKey>\r\n            <schema xmlns=\"\">ims</schema>\r\n        </createRequest>\r\n    </Body>\r\n</Envelope>".format(
#         description=description, title=title, key=key, category_id=category_id, category_name=category_name,
#         sub_category_id=sub_category_id, sub_category_name=sub_category_name)
#     headers = {
#         'Content-Type': 'text/xml',
#         'Authorization': 'Basic Zm1zX2ltc3VwcG9ydDpEYWxtaWFAMTIzNA=='
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload, verify=False)
#     from xml.etree import ElementTree
#     tree = ElementTree.fromstring(response.text)
#     return tree[0][0][0][29].text


# class SelfHelpVideos(Action):
#
#     def name(self) -> Text:
#         return "action_self_help_videos"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         text = "https://www.youtube.com/embed?v=qJDlttqmiXk&t=250s"
#         dispatcher.utter_message(text)
#         return [UserUtteranceReverted()]
#
# # class ActionUtterButton(Action):
#
#     def name(self) -> Text:
#         return "action_utter_buttons"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         buttons = [{"title": "Yes", "payload": "/yes"},
#                    {"title": "No", "payload": "/no"}]
#         dispatcher.utter_button_message("", buttons)
#
#         return [ActionReverted()]

class LoginForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        """Unique identifier of the form"""
        return "login_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["username", "password"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message or a list of them, where a first
                                     match will be picked"""

        y = {"username": self.from_text(intent=None),
             "password": self.from_text(intent=None)}
        return y

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        """Define what the form has to do
            	after all required slots are filleds"""
        buttons = [{"title": "Printer spooler", "payload": "/printerIssue"},
                   {"title": "Make Chrome Default", "payload": "/chromeDefault"},
                   {"title": "Slow Machine", "payload": "/slowMachine"}]
        return []


class ActionCreateTicketSpeedUp(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_speed_up_ticket_creation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Speed up machine")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketSetTimeToIst(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_set_time_to_IST_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Set time to ist")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]

        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketResolveBlueDumpError(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_resolve_blue_dump_error_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Blue Dump error")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketDisableJavaUpdate(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_resolve_disable_java_update_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Disable java Update")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketWindowIssue(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_window_update_issue_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Window issue")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketAntiVirus(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_antivirus_not_working_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Anti-virus not working")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketRemoteConnectionTroubleShooter(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_remote_connection_trouble_shooter_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Remote connection trouble shooter")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketBackupUserData(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_backup_user_data_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Back Up User Data")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketFreeUpDiskSpace(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_free_up_disk_space_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Free up disk space")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketUpdateGroupPolicy(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_update_group_policy_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Update group policy")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketSharedfolderForMapping(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_share_folder_for_mapping_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Share folder for mapping")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketAntiVirusNotWorking(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_anti_virus_not_working_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Anti virus is not working")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketUnableToOpenFile(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_unable_to_open_file_ticket_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "System - " + str("Unable to open jpg , png file")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# tickets for outlook


class ActionCreateTicketOutlookIsNotConnecting(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_outlook_is_not_connecting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Outlook - " + str("outlook is not connecting")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketCreateNewPSTArchiveFile(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_create_new_PST_archive_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Outook - " + str("Create new PST file archive")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketConfigureOutlook(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_configure_outlook"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Outlook - " + str("Configure outlook")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketPstFileSIze(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_pst_file_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Outlook - " + str("PST file size")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ActionCreateTicketOpenWebMail(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_open_web_mail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Outlook - " + str("Open Web mail")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# Create ticket for Browsers

class UnableToOpenPDFInIE(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_unable_to_open_PDF_in_IE"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Browser - " + str("Unable To Open PDF In IE")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class MakeChromeYourDefaultBrowser(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_make_chrome_default_browser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Browser - " + str("Make chrome default browser")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class SetInternetExplorerDefaultBrowser(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_internet_explorer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Browser - " + str("Internet Explorer Default Browser")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class MakeEdgeYourDefaultBrowser(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_Make_edge_your_Default_browser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Browser - " + str("Make Edge Default Browser")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# ticket create for connectivity_issues -----------


class LanNotWorking(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_lan_not_working"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Connectivity - " + str("Lan Not Working")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class UnableToConnectToWiFi(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_unable_to_Connect_to_Wi-Fi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Connectivity - " + str("Wi-Fi is not connecting")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ModifyTheHostsFileOnYourMachine(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_modify_the_hosts_file_on_your_machine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Connectivity - " + str("Modify the hosts file on your machine")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class InternetLANLimitedIssue(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_internetLANLimitedIssue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Connectivity - " + str("Internet LAN Limited Issue")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class CheckInternetWorkingOrNot(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_checkInternetWorkingOrNot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Connectivity - " + str("Check internet working Or not")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class checkInternetQualityAndSpeed(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_checkInternetQualityAndSpeed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Connectivity - " + str("Check internet quality and speed")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# create ticket for software


class CiscoWebexMeetingsInstallation(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_ciscoWebexMeetingsInstallation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Software - " + str("Cisco Webex Meetings Installation")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class GoogleChromeInstallation(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_GoogleChromeInstallation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Software - " + str("Google Chrome Installation")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class AdobeReaderInstallation(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_adobeReaderInstallation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Software - " + str("Adobe Reader Installation")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class WinRARInstallation(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_WinRARInstallation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Software - " + str("Win RAR Installation")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# ticket create for microssoft office

class SpeedUpMicrosoftPowerpoint(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_speedMicrosoftPowerpoint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Microsoft Office - " + str("Speed Up Microsoft Powerpoint")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class OfficeQuickRepair(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_officeQuickRepair"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Microsoft Office - " + str("Office Quick Repair")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ExcelFilesNotOpening(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_speedUpMicrosoftPowerpoint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Microsoft Office - " + str("Excel Files Not Opening")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ExcelRandomCrashIssues(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_excelRandomCrashIssues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Microsoft Office - " + str("Excel Random Crash Issues")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class ConvertWordFileIntoPdfFile(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_convertWordFileIntoPdfFile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Microsoft Office - " + str("Convert Word File Into Pdf File")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class OpenExcelInSafeMode(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_openExcelInSafeMode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Microsoft Office - " + str("Open Excel In Safe Mode")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# ticket for printer

class PrinterSpoolerServiceIsNotRunning(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_PrinterSpoolerServiceIsNotRunning"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Printer - " + str("Printer Spooler Service Is Not Running")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# ticket for ad service

class ResetYourPasswordFromAnywhere(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_resetYourPasswordFromAnywhere"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Ad Service - " + str("Reset Your Password From Anywhere")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class EnrollInADSelfServicePlusPortal(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_enrollInADSelfServicePlusPortal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Ad Service - " + str("Enroll In AD SelfService Plus Portal")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


# ticket for remote support
class JoinRemoteSupportSession(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_joinRemoteSupportSession"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Remote support - " + str("Join Remote Support Session")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]


class InstallRemoteSupportSoftware(Action):
    priority = ""

    def name(self) -> Text:
        return "action_ticket_creation_installRemoteSupportSoftware"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO Generic API integration
        subject = "Remote support - " + str("Install Remote Support Software")
        response = generate_rimcc_ticket(subject)  # ticket genertaion in rimcc
        if response.json()["operation"]["result"]["status"] == "Success":
            ticket_number = response.json()["operation"]["details"]["workorderid"]
            priority = response.json()["operation"]["details"]["priority"]
            sla = response.json()["operation"]["details"]["sla"]
            impact = response.json()["operation"]["details"]["impact"]
            subject = response.json()["operation"]["details"]["subject"]
        dispatcher.utter_message(
            "The following ticket has been created for you:-<br><br>Ticket Number:<a href='https://rimccsupport.teamcomputers.com/WorkOrder.do?woMode=viewWO&woID={}'>{}</a><br>Priority: {}<br>Subject: {}<br>Impact: {}<br>SLA: {}".format(
                ticket_number, ticket_number, priority, subject, impact, sla))

        # return [Restarted()]
        # return [UserUtteranceReverted()]
