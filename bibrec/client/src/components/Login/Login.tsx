import React, { useState } from "react";
import { User } from "../../App";
import "./Login.scss";

interface LoginProps {
	setUser: (user: User) => void;
	close: () => void;
}
export default function Login(props: LoginProps) {
	const { close, setUser } = props;

	const [userName, setUserName] = useState("");
	const [part, setPart] = useState(1);

	function nextPart(evt: React.MouseEvent<HTMLButtonElement, MouseEvent>) {
		setUser({ id: 1, username: userName });
		setPart(2);
	}
	return (
		<div className="login">
			{part == 1 ? (
				<div className="part1">
					<img src="/logo.png" width={120} alt="logo" />
					<h2>BibRec</h2>
					<p>Bitte gib deinen Benutzernamen ein:</p>
					<input
						className="line"
						type="text"
						name="userid"
						placeholder="Benutzernamen eingeben..."
						onChange={(e) => setUserName(e.target.value)}
					/>
					<div className="row">
						<button
							className="col skip"
							onClick={close}
							type="button"
						>
							Überspringen
						</button>
						<button
							className="col next"
							onClick={nextPart}
							type="button"
						>
							Weiter
						</button>
					</div>
				</div>
			) : (
				<div className="part2">
					<h3>
						Beantworte uns ein paar Fragen, damit wir dich besser
						kennen lernen
					</h3>
					<div>
						<label className="inputLabel" htmlFor="country">
							Aus welchem Land kommst du?
						</label>
						<input
							className="line"
							type="select"
							name="country"
							placeholder="Gib das Land in dem du wohnst ein"
							onChange={(e) => set}
						/>

						<label className="inputLabel" htmlFor="state">
							In welchem Bundesland wohnst du?
						</label>
						<input
							className="line"
							type="select"
							name="state"
							placeholder="Gib das Bundesland in dem du wohnst ein"
						/>

						<label className="inputLabel" htmlFor="city">
							In welcher Stadt wohnst du?
						</label>
						<input
							className="line"
							type="select"
							name="city"
							placeholder="Gib die Stadt in der du wohnst ein"
						/>

						<label className="inputLabel" htmlFor="age">
							Wie alt bist du?
						</label>
						<input
							className="line"
							type="text"
							name="age"
							placeholder="Gib dein Alter ein"
						/>
					</div>
					<div className="row">
						<button
							className="skip col"
							onClick={close}
							type="button"
						>
							Überspringen
						</button>
						<button
							className="col next"
							onClick={close}
							type="submit"
						>
							Weiter
						</button>
					</div>
				</div>
			)}
		</div>
	);
}
