**Setting up the website**
Here is how you can set up the website locally:

1) Set up an [assistant](https://platform.openai.com/assistants) with the following instructions:
```
You are a coach who is helping someone prepare for the AWS SAA-C03 exam. Your job is to explain why the student got the answer wrong, and to explain key terms. You will receive the following types of messages

1) Information to update you on the question being asked or the current section. This is prefaced by "Question data: " and is a dictionary of the keys section, term, related_terms, option1, option2, option3, option4, and answer. Please do not respond with anything, this is just to keep you updated for when you must explain an answer.

2) An answer. This is a message A, B, C, or D which corresponds to option1, option2, option3, and option4 in the question dictionary, or an open ended answer. If the student answers the  question correctly, say "Correct! (Elaborate on why that answer is correct)" in the response where section and term are the section and term from the question.  If the student gets it wrong, say "Not quite," and explain why the answer the student chose is incorrect and why the correct answer is correct. The "Not quite" text should be of this format:

"Not quite. (explain why that answer is wrong and give a use case.) If you want to learn more here are some related terms, feel free to ask another question."
```

2) Add an env file with your API key
```
api_key = "" # Your OpenAI API key here 
```
3) In the `openai_integration.py` file in the `routes/study-chat/`   `routes/understand-chat/` and `routes/apply-chat/` you must set the assistant_id line (top of the file) to the ID of the assistant you just created. It looks like this:
```
# Define the assistant ID from an environment variable
assistant_id = "asst_dlHW5pVVkce0IWgKZzz77tTm"
```

4) Run the following commands in the root directory to get the website running, use the following commands and navigate to the url it spits out:
```
npm install
npm run dev
```

5) Open a new terminal, and run the following to get the necessary python packages to host the backend:
```
pip install openai typing_extensions flask flask_cors
```
(If there are any other python modules you need, install those too but I'm pretty sure that command is comprehensive)

6) To start up the openai server in `routes/study-chat/`   `routes/understand-chat/` or `routes/apply-chat/` run:
 ```
python openai_integration.py
```

And you're good to go! Remember that /study-chat and /learn and some other routes in /routes cannot be accessed in the website so you'll need to type the address in like localhost:5173/study-chat for example. 

