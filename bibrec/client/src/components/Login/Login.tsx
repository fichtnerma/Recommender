import React, { Dispatch, SetStateAction, useState } from "react";
import { User, UserInfo } from "../../App";
import "./Login.scss";
import axios from "axios";

interface LoginProps {
	user?: User;
	setUser: Dispatch<SetStateAction<User>>;
	close: () => void;
}

export default function Login(props: LoginProps) {
	const { close, setUser, user } = props;

	const [userName, setUserName] = useState("");
	const [userInfo, setUserInfo] = useState<UserInfo | undefined>(user ? {
		country: user.country,
		state: user.state,
		city: user.city,
		age: user.age
	} : undefined);
	const [part, setPart] = useState(1);

	async function nextPart() {
		try {
			const res = await axios.post("http://localhost:4000/registerUser", {
				username: userName
			});
			const { user_id, city, country, state, age } = res.data as User;

			const user: User = {
				user_id: user_id,
				username: userName,
				country,
				state,
				city,
				age
			};

			setUser(user);
			setUserInfo({
				country,
				state,
				city,
				age
			});

			sessionStorage.setItem("user_id", user.user_id.toString());
			sessionStorage.setItem("username", user.username);
			country && sessionStorage.setItem("country", country);
			state && sessionStorage.setItem("state", state);
			city && sessionStorage.setItem("city", city);
			age && sessionStorage.setItem("age", age.toString());

			setPart(2);
		} catch (e) {
			console.error(e);
		}

	}

	async function onFormSubmit() {
		userInfo && setUser((prevUser) => ({ ...prevUser, ...userInfo }));

		userInfo?.country && sessionStorage.setItem("country", userInfo.country);
		userInfo?.state && sessionStorage.setItem("state", userInfo.state);
		userInfo?.city && sessionStorage.setItem("city", userInfo.city);
		userInfo?.age && sessionStorage.setItem("age", userInfo.age.toString());

		try {
			await axios.post("http://localhost:4000/registerUser", {
				username: userName,
				...userInfo
			});

		} catch (e) {
			console.error(e);
		}

		close();
	}

	return (
		<div className="login">
			{part == 1 ? (
				<div className="part1">
					<img src="/logo.png" width={120} alt="logo"/>
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
							disabled={!userName}
							aria-disabled={!userName}
							className="col next"
							onClick={() => {
								userName ? nextPart() : alert("Bitte gib einen Benutzernamen ein!");
							}}
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
							value={userInfo?.country || ""}
							onChange={(e) => setUserInfo({ ...userInfo, country: e.target.value })}
						/>

						<label className="inputLabel" htmlFor="state">
							In welchem Bundesland wohnst du?
						</label>
						<input
							className="line"
							type="select"
							name="state"
							placeholder="Gib das Bundesland in dem du wohnst ein"
							value={userInfo?.state || ""}
							onChange={(e) => setUserInfo({ ...userInfo, state: e.target.value })}
						/>

						<label className="inputLabel" htmlFor="city">
							In welcher Stadt wohnst du?
						</label>
						<input
							className="line"
							type="select"
							name="city"
							placeholder="Gib die Stadt in der du wohnst ein"
							value={userInfo?.city || ""}
							onChange={(e) => setUserInfo({ ...userInfo, city: e.target.value })}
						/>

						<label className="inputLabel" htmlFor="age">
							Wie alt bist du?
						</label>
						<input
							className="line"
							type="text"
							name="age"
							placeholder="Gib dein Alter ein"
							value={userInfo?.age || ""}
							onChange={(e) => setUserInfo({ ...userInfo, age: Number(e.target.value) })}
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
							onClick={onFormSubmit}
							type="button"
						>
							Weiter
						</button>
					</div>
				</div>
			)}
		</div>
	);
}
