import React from 'react';
import { Redirect } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function Homepage() {
  const { siteConfig } = useDocusaurusContext();
  return <Redirect to="/docs/introduction/physical-ai-foundations" />;
}

export default Homepage;