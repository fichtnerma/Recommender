import React, { useState } from 'react'
import "./Login.scss"

export default function Login(props: { close: () => void }) {
    const [part, setPart] = useState(1)
        return (
        <div className="login">
            {part == 1 ?
            <div className="part1">
                <img src="/logo.png" width={120} alt="logo"/>
                <h2>BibRec</h2>
                <p>Bitte gib deine Benutzer ID ein:</p>
                <input className="line" type="text" name="userid" />
                <div className="row">
                    <button className='col skip' onClick={props.close} type="button">Überspringen</button>
                    <button className='col next' onClick={nextPart} type="button">Weiter</button>
                </div>
            </div>
            :
            <div className="part2">
                <h3>Beantworte uns ein paar Fragen,damit wir dich besser kennen lernen</h3>
                <div>
                    <label className="line" htmlFor="country">Aus welchem Land kommst du?</label>
                    <input className="line" type="select" name="country" />
                    <label className="line" htmlFor="state">In welchem Bundesland wohnst du?</label>
                    <input className="line" type="select" name="state" />
                    <label className="line" htmlFor="city">In welcher Stadt wohnst du?</label>
                    <input className="line" type="select" name="city" />
                    <label className="line" htmlFor="age">Wie alt bist du?</label>
                    <input className="line" type="text" name="age" />
                </div>
                <div className="row">
                    <button className="skip col" onClick={props.close} type="button">Überspringen</button>
                    <button className="col next" type="submit">Weiter</button>
                </div>
            </div>}
        </div>
        )
    function nextPart(evt: React.MouseEvent<HTMLButtonElement, MouseEvent>) {
        setPart(2)
    }
}

