import { useState } from 'react'
import { v4 as uuidv4 } from "uuid";
// import { CreateStory, EditorStory, CapitolAiWrapper, generateStory } from "@capitol.ai/react";
import { EditorStory, CapitolAiWrapper, generateStory } from "@capitol.ai/react";

import './App.css'
import { BrowserRouter as Router, Routes, Route, Link, useParams } from "react-router-dom";

const config = {
  format: "auto_mode",
  cot: false,
  audience: "General",
  responseLength: "3 pages",
  responseLanguage: "english",
  heroImage: false,
  title: true,
  headers: true,
  paragraphs: true,
  images: false,
  aiImages: false,
  imageStyle: 'auto',
  aiGraphs: false,
  webGraphs: false,
  metrics: false,
  tables: false,
  quotes: false,
  tweets: false,
  tweetCharacterLimit: 280,
  generalWebSearch: true,
  academicWebSearch: false,
  usePerplexity: true,
  ragBudget: "default",
  customInstructions: 'Write a Technical Proposal for a grant project that demonstrates the applicant’s capability to implement the project in accordance with the announcement’s provisions. The proposal should be succinct, self-explanatory, and well-organized, covering all aspects of the proposed project. Include the following sections: Project Description (addressing the service area’s entrepreneurial ecosystem, measurable activities to support women entrepreneurs, key stakeholders and partners with proof of commitment, engagement with SBA resources, and efforts to engage underserved communities); Applicant Capability (organization profile, organizational background with experience and strategies, proof of capability to manage the project, project organizational structure with reporting and governance, and biographies or resumes for major participants); Data Collection and Program Evaluation (a data collection plan identifying specific data on participants, plans to document lessons learned, identification of effective service models for potential replication, and plans for using data to inform program delivery); Applicant Budget (including budget forms and a detailed expenditure worksheet with justification for all budget items); and Agency Priority Points (addressing at least two priorities such as promoting entrepreneurship among returning citizens, supporting rural entrepreneurial ecosystems, and increasing capacity of women to access government contracting opportunities). Ensure that the proposal aligns with the evaluation criteria, covers all years of the project period including the initial base and four option periods, and includes plans for required travel for key personnel to attend specified events.',
  imageHeight: 768,
  imageWidth: 1344,
  responseModel: 'claude-3-5-sonnet-20240620',
  userUrls: [],
  userPdfDocuments: [],
  userPdfUrls: [],
  userImages: [],
};


const Home = () => {
  const [storyIds, setStoryIds] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [userPrompt, setUserPrompt] = useState('Use the provided grantee profile to write a grant volume according to additional instructions.');
  
  const handleGenerateStory = async () => {
    setIsGenerating(true);
    const story = await generateStory({
      storyId: uuidv4(),
      userPrompt,
      storyPlanConfig: config,
    });
    story?.created?.id && setStoryIds((prev) => [...prev, story.created.id]);
    setIsGenerating(false);
  }

  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'row', gap: '10px', marginBottom: '10px' }}>
        <input type="text" value={userPrompt} onChange={(e) => setUserPrompt(e.target.value)} style={{ width: '100%', padding: '10px' }} disabled={isGenerating}  />
        <button onClick={handleGenerateStory} style={{ color: 'white', backgroundColor: 'black', padding: '10px 20px', borderRadius: '5px', width: '160px', flexShrink: 0 }} disabled={isGenerating}>{isGenerating ? 'Generating...' : 'Generate Story'}</button> 
      </div>
      {storyIds.map((storyId) => (
        <div key={storyId} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <Link to={`/story/${storyId}`}>Edit Story: {storyId}</Link>
        </div>
      ))}
    </div>
  );
}

const Editor = () => {
  const { storyId } = useParams();
  return <EditorStory storyId={storyId} />;
}

function App() {
  return (
    <CapitolAiWrapper>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/story/:storyId" element={<Editor />} />
        </Routes>
      </Router>
    </CapitolAiWrapper>
  );
}

export default App
