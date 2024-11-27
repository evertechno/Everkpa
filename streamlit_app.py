import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Knowledge Process Automation (KPA) as a Service")
st.write("Automate complex, knowledge-intensive tasks using Generative AI, RPA, AI, and ML.")

# Input: Select task type
task_type = st.selectbox("Select the task you want to automate:", [
    "Document Summarization", 
    "Customer Query Response", 
    "Data Extraction", 
    "Report Generation", 
    "Task Scheduler", 
    "API Integration"
])

# Inputs based on selected task
if task_type == "Document Summarization":
    document_text = st.text_area("Paste the document to summarize:")
elif task_type == "Customer Query Response":
    prompt = st.text_input("Enter your query:", "What is the status of my order?")
elif task_type == "Data Extraction":
    data = st.text_area("Provide the data to extract insights from:")
elif task_type == "Report Generation":
    data_points = st.text_area("Provide the data for the report generation:")
elif task_type == "Task Scheduler":
    schedule_time = st.time_input("Schedule time for task (HH:MM):", value=datetime.now().time())
    task_action = st.selectbox("Select the task to schedule:", ["Summarize document", "Generate report", "Extract data"])
elif task_type == "API Integration":
    api_endpoint = st.text_input("Enter API endpoint to integrate with:")
    api_method = st.selectbox("Select API method", ["GET", "POST"])

# Button to start the task automation
if st.button("Start Automation"):
    with st.spinner("Processing... Please wait while the task is being automated..."):
        try:
            # If Document Summarization
            if task_type == "Document Summarization" and document_text:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Summarize this document: {document_text}")
                st.write("Summary:")
                st.write(response.text)

            # If Customer Query Response
            elif task_type == "Customer Query Response" and prompt:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Answer this query: {prompt}")
                st.write("Response:")
                st.write(response.text)

            # If Data Extraction
            elif task_type == "Data Extraction" and data:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Extract key insights from this data: {data}")
                st.write("Extracted Insights:")
                st.write(response.text)

            # If Report Generation
            elif task_type == "Report Generation" and data_points:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Generate a report based on this data: {data_points}")
                st.write("Generated Report:")
                st.write(response.text)

            # If Task Scheduler
            elif task_type == "Task Scheduler":
                task_time = schedule_time.strftime("%H:%M")
                st.write(f"Task scheduled for {task_time}. We'll notify you once it's done!")
                # Here you could integrate a task scheduler like Celery or use Python's `schedule` module for real scheduling.
                # For simplicity, we'll just simulate a notification in this example.
                time.sleep(5)
                st.write(f"Task scheduled at {task_time} has been completed!")  # Simulated success message

            # If API Integration (Sending HTTP request)
            elif task_type == "API Integration" and api_endpoint:
                if api_method == "GET":
                    response = requests.get(api_endpoint)
                elif api_method == "POST":
                    response = requests.post(api_endpoint)
                st.write("API Response:")
                st.write(response.json())

            # Handle case where no input is provided
            else:
                st.warning("Please provide the required input for the selected task.")

            # Example of storing the result in a CSV (as a placeholder for a database)
            result = {
                "Task": task_type,
                "Input": document_text if task_type == "Document Summarization" else prompt if task_type == "Customer Query Response" else data if task_type == "Data Extraction" else data_points,
                "Result": response.text if task_type in ["Document Summarization", "Customer Query Response", "Data Extraction", "Report Generation"] else str(response.json())
            }
            df = pd.DataFrame([result])
            df.to_csv("automation_results.csv", mode="a", header=False, index=False)  # Append to CSV file

            st.write("Result has been saved.")

        except Exception as e:
            st.error(f"Error: {e}")

# Function to send an email notification (Example: Notify about task completion)
def send_email_notification(subject, body, to_email):
    try:
        sender_email = st.secrets["EMAIL_SENDER"]
        sender_password = st.secrets["EMAIL_PASSWORD"]
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        st.success(f"Email sent to {to_email}.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Example: Send notification email when task is complete
if st.button("Send Task Completion Email"):
    send_email_notification(
        subject="KPA Task Completed",
        body="Your Knowledge Process Automation task has been completed successfully.",
        to_email="recipient@example.com"  # Change to the recipient's email
    )
