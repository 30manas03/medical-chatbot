# Medical Chatbot Deployment Guide

## Deploying to Render

This guide will help you deploy your medical chatbot to Render successfully.

### Prerequisites

1. **API Keys Required:**
   - `PINECONE_API_KEY` - Your Pinecone API key for vector database
   - `GROQ_API_KEY` - Your Groq API key for the LLM

2. **Pinecone Index:**
   - Ensure your Pinecone index "medical-chatbot-1" is already created and populated with medical data

### Deployment Steps

#### 1. Prepare Your Repository

The following files have been created/updated for deployment:
- `render.yaml` - Render deployment configuration
- `Procfile` - Alternative deployment method
- `runtime.txt` - Python version specification
- `app.py` - Updated to use PORT environment variable

#### 2. Deploy to Render

1. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" and select "Web Service"

2. **Configure the Service:**
   - **Name:** medical-chatbot
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Set Environment Variables:**
   - Go to the "Environment" tab
   - Add the following environment variables:
     - `PINECONE_API_KEY` = Your Pinecone API key
     - `GROQ_API_KEY` = Your Groq API key

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

#### 3. Alternative Deployment (Using render.yaml)

If you prefer to use the `render.yaml` file:

1. **Connect Repository:**
   - In Render, select "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

2. **Set Environment Variables:**
   - After the service is created, go to the service settings
   - Add your API keys in the Environment Variables section

### Troubleshooting

#### Common Issues:

1. **Build Failures:**
   - Check that all dependencies in `requirements.txt` are compatible
   - Ensure Python version is correct (3.9.16)

2. **Runtime Errors:**
   - Verify API keys are correctly set in environment variables
   - Check that Pinecone index exists and is accessible

3. **Port Issues:**
   - The app is configured to use the `PORT` environment variable provided by Render
   - No manual port configuration needed

4. **Memory Issues:**
   - The free tier has memory limitations
   - Consider upgrading to a paid plan for better performance

#### Environment Variables Checklist:

- [ ] `PINECONE_API_KEY` - Your Pinecone API key
- [ ] `GROQ_API_KEY` - Your Groq API key
- [ ] `PORT` - Automatically set by Render

### Post-Deployment

1. **Test the Application:**
   - Visit your deployed URL
   - Test the chat functionality
   - Verify that medical queries are working

2. **Monitor Logs:**
   - Check Render logs for any errors
   - Monitor API usage and costs

3. **Custom Domain (Optional):**
   - Add a custom domain in Render settings
   - Configure DNS settings

### Security Notes

- Never commit API keys to your repository
- Use environment variables for all sensitive data
- Regularly rotate your API keys
- Monitor API usage to control costs

### Cost Optimization

- Free tier has limitations on requests and memory
- Monitor your Groq and Pinecone usage
- Consider upgrading plans based on usage

### Support

If you encounter issues:
1. Check Render logs for error messages
2. Verify all environment variables are set correctly
3. Test locally before deploying
4. Contact Render support for platform-specific issues 