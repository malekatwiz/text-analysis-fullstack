// src/pages/NewJob.js
import React, { useState } from 'react';
import axios from 'axios';

const VITE_JOBS_API_URL = 'http://localhost:8080'

function NewJob() {
  const [sourceLink, setSourceLink] = useState('');
  const [jobContent, setJobContent] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(`${VITE_JOBS_API_URL}/jobs/postings`, {
        description: jobContent,
        source_link: sourceLink
      });
      console.log('Job submitted successfully:', response.data);
      alert('Job submitted successfully!');
      // Clear the textarea after submission
      setJobContent('');
      setSourceLink('');
    } catch (error) {
      console.error('Error submitting job:', error);
      alert('Failed to submit job. Please try again.');
    }
  };

  return (
    <div className="page-content">
      <h2>Add a New Job</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="source-link">Source Link:</label>
          <input
            type="text"
            id="source-link"
            value={sourceLink}
            onChange={(e) => setSourceLink(e.target.value)}
            style={{ width: '100%' }}
            required
          />
          <label htmlFor="job-content">Description:</label>
          <textarea
            id="job-content"
            value={jobContent}
            onChange={(e) => setJobContent(e.target.value)}
            style={{ width: '100%' }}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default NewJob;