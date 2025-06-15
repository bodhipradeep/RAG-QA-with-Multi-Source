# AWS Deployment Instructions for RAG QA Chatbot

These are the step-by-step instructions to deploy the chatbot on an AWS EC2 instance.

---

## 1. Launch EC2 Instance

- Region: `eu-north-1`
- Go to: [AWS EC2 Dashboard](https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#Home:)
- Click **"Launch Instance"**
- Name: `RAG QA Chatbot` (or any)
- Keep default OS (Amazon Linux)
- Select existing Key Pair (or create a new one and save the `.pem` file)
- Keep all defaults and launch the instance

---

## 2. Connect to EC2

- After launch, AWS will show your Instance ID
- Click the **Instance ID**
- Use the checkbox and click **Connect**
- Use the browser-based SSH (or copy public IP to connect via terminal)

---

## 3. Setup via SSH

```bash
# Update packages
sudo yum update -y

# Install Git and Python
sudo yum install git -y
sudo yum install pip -y

# Clone GitHub repo
git clone https://github.com/bodhipradeep/RAG-QA-with-Multi-Source.git
cd RAG-QA-with-Multi-Source

# Install Python requirements
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

## 4. Allow Incoming Traffic (If App Doesn't Load)
If http://<your-public-ip>:8501 doesn't load:
Go to EC2 → Click on Instance ID → Security → Security Groups → Edit Inbound Rules
Click "Edit inbound rules"
Add rule:
Type: All Traffic
Source: Anywhere
Save changes and reload the public IP in your browser
