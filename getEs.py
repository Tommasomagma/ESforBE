from openai import OpenAI

def gptEs(imageUrl, problemDescription, correctAnswer, userAnswer, hint):

    #I will give you the code separately
    try:
        client = OpenAI(api_key='X')

        #Prompt for errorspotting
        prompt = (
            """Goal: Look closely at the student's drawing and identify the part of the solution that should be highlighted for the student to realize where the following hint should be applied. 
            This means that the part of the solution you highlight is the part of the solution where the student can realize what the hint is referring to. 
            Use the red smaller digits in the image of the student's solution to highlight the error concerned by the hint. 
            You should only return a list with the indices around the part you wish to highlight. That means that your output should only include [a,b,c] where a,b,c… are the indices you wish to highlight.\n\n"""
            """Warnings: Ignore the smaller digits written in red and only consider the black/grey, handwritten characters as the mathematical part of the student's solution. 
            If the hint is based on general aspects of the problem and how to solve it rather than a specific part present in the solution make sure you don't highlight anything.\n\n"""
            """Context: If the hint suggests that elements from the problem descriptions are written down incorrectly, such as the solution '2-1=1' when the problem is '2+1=?', you should highlight the area around '+' since this is incorrect. 
            If the mathematical expression written down is the correct one for finding the answer but the hint suggests that the answer ends up being incorrect due to miscalculations, you should highlight the answer, 
            such as solution 'x-2=3 x=3+2 x=6' for problem 'find x for x-2=3' where you should highlight '6'. If the hint suggests that the mathematical expression written down will not lead to the correct answer, you should highlight the part of the mathematical expression which is incorrect, 
            such as solution 'x-2=3 x=3-2 x=1' for problem 'find x for x-2=3' where you should highlight '3-2'.\n\n"""
            """Return format: Try to include at least 2-3 indices in the part you highlight, but try to include a higher amount of indices to make sure the error is included in the highlighted part. 
            Make sure you highlight indices which are spatially adjacent in the image.\n\n"""
            f"""The problem description is {problemDescription} to which the correct answer is: {correctAnswer}. The student's hand-written solution can be seen in the Image.
            The incorrect answer they submitted is: {userAnswer}. The hint you should map to a part of the solution is: {hint}."""
        )

        # Prepare the input for OpenAI API with both text and image 
        response = client.chat.completions.create(
                
                #I will give you the model ID separately
                model = 'fineTunedModel',
                
                messages= [
                    {
                    "role": "system",
                    "content": prompt,
                    },
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "image_url",
                        "image_url": {
                            "url":imageUrl
                        }
                        }
                    ]
                    }
                ],
                max_tokens=250 
            )

        # Extract the classification from the response
        index = response.choices[0].message.content.strip()

    except Exception as e:
        return -1

    return index