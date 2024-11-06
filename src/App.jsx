import { useState } from 'react'
import { v4 as uuidv4 } from "uuid";
// import { CreateStory, EditorStory, CapitolAiWrapper, generateStory } from "@capitol.ai/react";
import { EditorStory, CapitolAiWrapper, generateStory } from "@capitol.ai/react";

import './App.css'
import { BrowserRouter as Router, Routes, Route, Link, useParams } from "react-router-dom";

const technicalReportConfig = {
  format: "custom",
  cot: true,
  audience: "General",
  responseLength: "",
  responseLanguage: "english",
  heroImage: false,
  title: false,
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
  generalWebSearch: false,
  academicWebSearch: false,
  usePerplexity: false,
  ragBudget: "default",
  customInstructions: "Please create a Technical Proposal demonstrating your capability to implement the grant project, organized with the following sections: 1) **Project Description** (50 points), detailing services in counseling, training, access to capital, and knowledge transfer, including defining your geographic area and entrepreneurial ecosystem, describing measurable activities to support women entrepreneurs, identifying key stakeholders and partners with proof of third-party commitments, explaining how you will engage with SBA resources, and addressing efforts to engage women entrepreneurs from underserved communities; 2) **Applicant Capability** (25 points), providing a concise summary of your organization\u2019s mission, programs, relevant experience, proof of capability including financial and management infrastructure, organizational structure with duties and reporting, and one-page biographies or resumes of key personnel; 3) **Data Collection and Program Evaluation** (25 points), outlining your data collection plan including specific participant data and collection methods, plans to document lessons learned, identification of effective service models for potential replication, and how data will inform program delivery; 4) **Applicant Budget** (10 points), including the required Standard Forms SF-424 and SF-424A, and a Detailed Expenditure Worksheet with detailed justification for all budget items; and 5) **Agency Priority Points** (10 points), addressing at least two of SBA's priority areas such as promoting entrepreneurship among returning citizens, supporting rural entrepreneurial ecosystems, or increasing women's capacity to access government contracting opportunities, describing current efforts, past results, and execution plans through the WBC project. Ensure all required attachments, such as proof of third-party commitments and resumes, are included, and incorporate required travel costs for key personnel to attend specified events.",
  imageHeight: 768,
  imageWidth: 1344,
  responseModel: 'claude-3-5-sonnet-20240620',
  userUrls: ['https://gist.github.com/zstone-cai/323e78d0b0e0f9f312105d2c1595bcbd'],
  userPdfDocuments: [],
  userPdfUrls: [],
  userImages: [],
};

const abstractReportConfig = {
  format: "custom",
  cot: false,
  audience: "General",
  responseLength: "1 page",
  responseLanguage: "english",
  heroImage: false,
  title: false,
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
  generalWebSearch: false,
  academicWebSearch: false,
  usePerplexity: false,
  ragBudget: "default",
  customInstructions: "Please generate an abstract of no more than one page summarizing the proposed project, including the scope of the project and proposed outcomes. The abstract must include the following sections: 1) Applicant's name; 2) Designated point of contact's telephone number and email address; 3) Web address; 4) Project title; 5) Description of the area to be served; 6) Number of participants to be served; and 7) Funding level requested.",
  imageHeight: 768,
  imageWidth: 1344,
  responseModel: 'claude-3-5-sonnet-20240620',
  userUrls: ['https://gist.github.com/zstone-cai/323e78d0b0e0f9f312105d2c1595bcbd'],
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
    const story1 = await generateStory({
      storyId: uuidv4(),
      userPrompt,
      storyPlanConfig: abstractReportConfig,
    });
    setTimeout(async () => {
      const story2 = await generateStory({
        storyId: uuidv4(),
      userPrompt,
        storyPlanConfig: technicalReportConfig,
      });
      story1?.created?.id && setStoryIds((prev) => [...prev, story1.created.id]);
      story2?.created?.id && setStoryIds((prev) => [...prev, story2.created.id]);
      setIsGenerating(false);
    }, 2000);
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
