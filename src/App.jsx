import { useState } from 'react'
import { CreateStory, EditorStory, CapitolAiWrapper } from "@capitol.ai/react";

import './App.css'

function App() {
  const [currentStoryId, setCurrentStoryId] = useState();
  const handleCallback = (storyId) => setCurrentStoryId(storyId);

  return (
    <CapitolAiWrapper>
      {!currentStoryId 
        ? <CreateStory callbackOnSubmit={handleCallback} pageTitle="Capitol AI" />
        : <EditorStory storyId={currentStoryId} />
      }
    </CapitolAiWrapper>
  );
}

export default App
