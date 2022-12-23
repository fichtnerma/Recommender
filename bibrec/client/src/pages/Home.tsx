import React, { useEffect, useState } from "react";
import BookDetailModal from "../components/BookDetails/BookDetailModal";
import "./Home.scss";
import { User } from "../App";
import { BooksBlock } from "../components/Books/BooksBlock";
import axios from "axios";
import { Book, Rating } from "../types/types";
import { getTimezoneCountry } from "../../utils/utils";

interface HomeProps {
	user?: User;
}

export default function Home({ user }: HomeProps) {
	const [userRecommendations, setUserRecommendations] = useState<Book[]>([]);
	const [isUserRecError, setIsUserRecError] = useState<boolean>(false);
	const [topInCountry, setTopInCountry] = useState<Book[]>([]);
	const [browseBooks, setBrowseBooks] = useState<Book[]>([]);
	const [userRatings, setUserRatings] = useState<Rating[]>([]);
	const [modalVisible, setModalVisible] = useState(false);
	const [selectedBook, setSelectedBook] = useState<undefined | Book>(
		undefined
	);

	useEffect(() => {
		try {
			if (user) {
				axios.get("http://localhost:4000/ratings", { params: { userId: user?.user_id } })
					.then((res) => {
						setUserRatings(res.data);
					});

				user.age && user.country && getUserRecommendations();
			}

			const timezoneCountry = getTimezoneCountry();

			!topInCountry.length && axios.post("http://localhost:4000/topInCountry", {
				userId: user?.user_id,
				recommendationCount: 20,
				timezoneCountry
			}).then((res) => {
				setTopInCountry(res.data);
			});

			!browseBooks.length && axios.post("http://localhost:4000/browse")
				.then((res) => {
					setBrowseBooks(res.data);
				});


		} catch (e) {
			console.error(e);
		}
	}, [user]);

	useEffect(() => {
		userRatings.length >= 5 && !userRecommendations.length && getUserRecommendations();
	}, [userRatings]);

	function getUserRecommendations() {
		return axios.post("http://localhost:4000/userRecommendations", {
			userId: user?.user_id,
			recommendationCount: 20
		}).then((res) => {
			setIsUserRecError(false);
			setUserRecommendations(res.data);
		}).catch(() => setIsUserRecError(true));
	}

	function onItemClick(book: Book) {
		setModalVisible(true);
		setSelectedBook(book);
	}

	return (
		<div className="wrapper">
			{modalVisible && selectedBook ? (
				<BookDetailModal
					setSelectedBook={setSelectedBook}
					selectedBook={selectedBook}
					onClose={setModalVisible}
					userRatings={userRatings}
					setUserRatings={setUserRatings}
					user={user}
				/>
			) : null}

			{user && !isUserRecError && (userRatings.length >= 5 || (user.country && user.age)) ?
				<BooksBlock title={"Deine Empfehlungen"} items={userRecommendations} onItemClick={onItemClick}/> : null}

			<BooksBlock title={"Top Bücher in deinem Land"} items={topInCountry} onItemClick={onItemClick}/>

			<BooksBlock title={"Mehr erkunden"} items={browseBooks} onItemClick={onItemClick}/>
		</div>
	);
}
