import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import Login from './components/Login/Login'
import Home from './pages/Home'
import Header from './components/Header/Header'
import Modal from './components/Login/Modal'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
        <Header/>
        <Modal />
        <Home/>
    </div>
  )
}

export default App
