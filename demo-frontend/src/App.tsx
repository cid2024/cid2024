import ProblemViewer from './components/problemViewer'
import './App.css'
import ProblemJSON from './components/problem.json';

function App() {

  return (
    <>
      <ProblemViewer
        array={ProblemJSON}
        width={120}
        disablePink={false}
      />
    </>
  )
}

export default App
