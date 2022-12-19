import React, { useEffect, useState } from "react";
import BookDetailModal from "../components/BookDetails/BookDetailModal";
import { Book } from "../components/Books/BookItem";
import "./Home.scss";
import { User } from "../App";
import { BooksBlock } from "../components/Books/BooksBlock";
import axios from "axios";

interface HomeProps {
	user?: User;
}

export default function Home({ user }: HomeProps) {
	const [userRecommendations, setUserRecommendations] = useState<Book[]>([]);
	const [topInCountry, setTopInCountry] = useState<Book[]>([]);
	const [browseBooks, setBrowseBooks] = useState<Book[]>([]);
	const [modalVisible, setModalVisible] = useState(false);
	const [selectedBook, setSelectedBook] = useState<undefined | Book>(
		undefined
	);

	useEffect(() => {
		if (user) {
			try {
				axios.post("http://localhost:4000/userRecommendations", {
					userId: user?.id,
					recommendationCount: 20
				}).then((res) => {
					setUserRecommendations(res.data);
				});

				axios.post("http://localhost:4000/topInCountry", {
					userId: user?.id,
					recommendationCount: 20,
					browserLang: navigator.language
				}).then((res) => {
					setTopInCountry(res.data);
				});

				axios.post("http://localhost:4000/browse")
					.then((res) => {
						setBrowseBooks(res.data);
					});

			} catch (e) {
				console.error(e);
			}
		}
	}, [user]);

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
					user={user}
				/>
			) : null}

			{user ?
				<BooksBlock title={"Deine Empfehlungen"} items={userRecommendations} onItemClick={onItemClick}/> : null}

			<BooksBlock title={"Top 5 in deinem Land"} items={topInCountry} onItemClick={onItemClick}/>

			<BooksBlock title={"Mehr erkunden"} items={browseBooks} onItemClick={onItemClick}/>
		</div>
	);
}
