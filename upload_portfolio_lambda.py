import boto3
import boto3
import botocore
import StringIO
import zipfile
import mimetypes
from botocore.client import Config

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic("arn:aws:sns:us-east-1:754984481887:deployPortfolio")
    try:
        s3 = boto3.resource('s3',config = Config(signature_version='s3v4')
        )
        portfolio_bucket = s3.Bucket('karla.portfolio')
        build_bucket = s3.Bucket('karlabuild.portfolio')
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('buildPortfolio', portfolio_zip)
        
        
        with zipfile.ZipFile(portfolio_zip) as myzip :
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    
        topic.publish(Subject="Portfolio deployed", Message = "Portfolio deployed successfully")
    except:
        topic.publish(Subject='Portfolio deployment failed', Message='The portfolio was not deployed successfully!')
        raise
        
    return "Hello from lambda"
