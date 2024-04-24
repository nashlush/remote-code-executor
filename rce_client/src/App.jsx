import { useState } from 'react'
import EditorBox from './components/EditorBox'

function App() {

  const defaultValues = {
    javascript: '// Welcome to JavaScript',
    java: '// Welcome to Java',
    python: '# Welcome to Python',
    cpp: '// Welcome to C++',
  };

  const defaultLanguage = "javascript"

  return (
    <>
      <EditorBox defaultLanguage={defaultLanguage} defaultValues={defaultValues} />
    </>
  )
}

export default App
