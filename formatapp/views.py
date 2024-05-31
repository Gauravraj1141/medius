from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from django.core.mail import EmailMessage
from django.template.loader import get_template
import base64

from django.conf import settings
EMAIL_ADMIN  = settings.EMAIL_HOST_USER
FROM_NAME = "Gaurav Rajput"

def send_summary_to_hr(request):
    summary_data = request
    message = get_template("formatapp/email_template.html").render({
        'data': summary_data
    })
    mail = EmailMessage(
        subject= "Summary report for the uploaded data",
        body=message,
        # from_email=EMAIL_ADMIN,
        from_email=f"{FROM_NAME} <{EMAIL_ADMIN}>",
        to=[summary_data['email']],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    return mail.send()


def uploadfile(request):

    return render(request, "formatapp/upload_file.html")
   
def formatfile(request):
    if request.method == 'GET':
        return redirect("uploadfile")
    
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
       
        # Check file type and read content
        file_name = uploaded_file.name
        file_extension = file_name.split('.').pop().lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension == 'xlsx':
            df = pd.read_excel(uploaded_file)
        else:
            messages.error(request, 'Unsupported file type. Please upload a CSV or XLSX file.')
            return render(request, "formatapp/upload_file.html")
        
        # Create a set of unique customer states
        file_data = df.copy()
        file_data.rename(columns={'Cust State': 'State'}, inplace=True)
        # Group by 'Cust State' and 'DPD' and count occurrences
        dpd_counts = file_data.groupby(['State', 'DPD']).size().reset_index(name='Count')


        

        dpd_count_dataframes = dpd_counts.to_html(classes='table table-striped table-bordered', index=False)
        
        for email in ['tech@themedius.ai',"hr@themedius.ai","gamergaurav1141@gmail.com"]:
            email_content = {}
            email_content['email'] = email
            email_content['summary_data'] = dpd_count_dataframes
            send_summary_to_hr(email_content)
        
        
        

        context = {'final_dataframes': dpd_count_dataframes}
        messages.success(request, 'File uploaded successfully. Check your email for the summary report.')
        
        return render(request, "formatapp/upload_file.html", context)
    return render(request, "formatapp/upload_file.html")