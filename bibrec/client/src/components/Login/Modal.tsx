import React, { useState } from 'react'
import Login from './Login'
import "./Login.scss"

export default function Modal() {
    const [visible, setVisible] = useState(true) 
  return (
    visible ?
    <div className="modalBackground">
        <div className='modal'>
            <Login close={() => setVisible(false)}></Login>
        </div>
    </div>
    : null
  )
}
