# MedTrack AWS Deployment Guide

## Prerequisites
- AWS Account
- AWS CLI installed and configured
- Docker installed locally

## Step 1: Set up MongoDB Atlas (Cloud Database)
1. Go to https://cloud.mongodb.com/
2. Create a free cluster
3. Create a database user
4. Whitelist your IP (0.0.0.0/0 for testing)
5. Get the connection string: `mongodb+srv://username:password@cluster.mongodb.net/medtrack`

## Step 2: Build and Push Docker Image to ECR
```bash
# Build the image
docker build -t medtrack .

# Tag for ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag medtrack:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medtrack:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medtrack:latest
```

## Step 3: Deploy to EC2
1. Launch EC2 instance (t2.micro for free tier)
2. Install Docker on EC2
3. Pull and run the container:
```bash
docker run -d -p 80:5000 -e MONGO_URI="your_mongodb_atlas_uri" YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medtrack:latest
```

## Step 4: Configure Security Groups
- Open port 80 (HTTP) in EC2 security group

## Step 5: Access Your Application
- Public IP of EC2 instance

## Future Enhancements
- Add SSL with AWS Certificate Manager
- Use Elastic Load Balancer
- Implement auto-scaling
- Add S3 for file storage
- Integrate AI features