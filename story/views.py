from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import shortStory
import os
from groq import Groq
from .models import Prompts
from django.contrib import messages
from django.shortcuts import redirect


class EditorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id=None):
        title = request.data.get('title', '').strip()
        content = request.data.get('content', '').strip()
        print(story_id)
        if not title or not content:
            return Response({'error': 'Title and content are required.'}, status=400)

        if story_id:
            story = get_object_or_404(shortStory, id=story_id, author=request.user)
            story.storyTitle = title
            story.content = content
            story.save()
            messages.success(request, 'Story updated successfully!')
            return redirect('/feed/')
        else:
            story = shortStory.objects.create(
                storyTitle=title,
                content=content,
                author=request.user
            )
            messages.success(request, 'Story created successfully!')
            return redirect('/feed/')


    def get(self, request, story_id=None):
        print(story_id)
        if story_id:
           
            story = get_object_or_404(shortStory, id=story_id, author=request.user)
            context = {
                'title': story.storyTitle,
                'content': story.content,
                'story_id': story.id
            }
            print("rendering edit-editor")
            return render(request, 'edit-editor.html', context)
        else:
           
            context = {
                'title': '',
                'content': '',
                'story_id': None
            }
            print("rendering editor")
            return render(request, 'editor.html', context)

     
            
    
class PromptEngineView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'prompts.html')
    
    def post(self, request):
        action_type = request.POST.get('action-type')
        context = request.POST.get('context')
        print(action_type)
        print(context)
        if action_type == 'specific' and context:
            # Generate a prompt based on user input
            prompt = self.generate_prompt_from_context(context)
            print(prompt)
            Prompts.objects.create(context_prompt=prompt)
        
        elif action_type == 'random':
            # Generate a prompt based on user input
            prompt = self.generate_prompt_without_context()
            print(prompt)
            Prompts.objects.create(random_prompt=prompt)
        
        else:
            prompt = "Please enter a valid prompt and try again"

        return render(request, 'prompts.html', {'prompt': prompt})
        
        
    def generate_prompt_from_context(self, context):
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
                        Generate a single story prompt for writers to build a story upon. 
                        Only provide the prompt directly and no other tags.
                        The prompts should include a variety of genres such as mystery, sci-fi, fantasy, romance, thriller, historical fiction, and contemporary drama. 
                        In addition to different genres, include themes like adventure, moral dilemmas, coming-of-age, betrayal, and redemption.
                        Ensure the prompts have a variety of formats:
                        1. Plot-driven prompts.
                        2. Beginning-of-story prompts.
                        3. End-of-story prompts that hint at a twist or resolution.
                        4. Situational prompts that challenge the writer to think creatively and build a story from a unique perspective.

                        The prompts should be varied in writing style, taking inspiration from different famous authors
                        Each prompt should be concise and limited to a maximum of 60 words.
                        IMPORTANT: Use this context to generate the prompt {context}
                        '''
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    
    def generate_prompt_without_context(self):
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
                        Generate a single story prompt for writers to build a story upon. 
                        Only provide the prompt directly and no other tags.
                        The prompts should include a variety of genres such as mystery, sci-fi, fantasy, romance, thriller, historical fiction, and contemporary drama. 
                        In addition to different genres, include themes like adventure, moral dilemmas, coming-of-age, betrayal, and redemption.
                        Ensure the prompts have a variety of formats:
                        1. Plot-driven prompts.
                        2. Beginning-of-story prompts.
                        3. End-of-story prompts that hint at a twist or resolution.
                        4. Situational prompts that challenge the writer to think creatively and build a story from a unique perspective.

                        The prompts should be varied in writing style, taking inspiration from different famous authors 

                        Each prompt should be concise and limited to a maximum of 60 words.
                        '''
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
        

class StoryDeleteView(APIView):

    def post(self, request, story_id):
        # Get the story object to delete
        story = get_object_or_404(shortStory, id=story_id)

        # Ensure the user is the owner of the story
        if story.author != request.user:
            messages.error(request, "You do not have permission to delete this story.")
            return redirect('profile') 

        story.delete()
        
        messages.success(request, "Story deleted successfully.")
        
        return redirect('profile') 


