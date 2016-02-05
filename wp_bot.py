import smtplib
import praw
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

r = praw.Reddit(user_agent = "Read day's top comments from /r/writing_prompts and save them in google drive")

def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')
    dt = str(datetime.date.today());
    main_content = str(markdown2.markdown(dt + u'\n'));
    print("Got the date...")
    me = "email.id@gmail.com"
    you = "email.id+wp@gmail.com";
    pswd = "password";
    subreddit = r.get_subreddit("writingprompts")
    print("Got the subreddit...")
    submissions = subreddit.get_top_from_day(limit=5)
    for sinx, submission in enumerate(submissions, start=1):
        wp = submission.title.encode('utf8');
        main_content= main_content + u'<p><h2>' + str(markdown2.markdown(str(sinx) + u'. ' + wp + u'\n')) + u'<h2>'
        cont = r.get_submission(submission_id=submission.id, comment_limit=3, comment_sort='top');
        cont.replace_more_comments(limit=2, threshold=0)
        for cinx, comment in enumerate(cont.comments[:3], start=1):
            main_content= main_content + u'<p>' + str(markdown2.markdown(u'\t' + str(cinx) + u'. ' + comment.body.encode('utf8') + u'\n')) + u'<br></p>';
        main_content= main_content + u'</p>'
    print("Got the submissions and comments...")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Writing Prompts: " + dt
    msg['From'] = me
    msg['To'] = you
    html = """\
	<html>
	  <head></head>
	  <body>
		<p> {main_content}
		</p>
	  </body>
	</html>
	""".format(main_content=main_content)
    part = MIMEText(html, 'html')
    msg.attach(part)
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(me, pswd)
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
    print("Sent the email...")    
if __name__ == "__main__":
    main()