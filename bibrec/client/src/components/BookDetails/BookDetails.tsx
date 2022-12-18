import React from "react";
import { Book } from "../Books/BookItem";
import Rating from "../Books/Rating";
import "./BookDetails.scss";
import { User } from "../../App";
import axios from "axios";

interface BookDetailsProps {
	selectedBook: Book;
	setSelectedBook: (value: Book) => void;
	user?: User;
}

export default function BookDetails({ selectedBook, user, setSelectedBook }: BookDetailsProps) {
	const { imageUrlLarge, author, rating_mean, rating_count, title, pubYear } = selectedBook;

	function onRate(selectedRating: number) {
		const sendRating = confirm(`Möchtest du das Buch „${title}“ wirklich mit ${selectedRating} Sternen bewerten?`);
		if (sendRating) {
			try {
				axios.post("http://localhost:4000/rateBook", {
					userId: user?.id,
					isbn10: selectedBook.isbn10,
					rating: selectedRating
				}).then(() => {
					const { rating_count, rating_mean } = selectedBook;
					const updatedCount = rating_count + 1;
					const updatedMean = (rating_count * rating_mean + 1 * selectedRating) / (rating_count + 1);
					setSelectedBook({ ...selectedBook, rating_count: updatedCount, rating_mean: updatedMean });
				});

			} catch (e) {
				console.error(e);
			}
		}
	}

	return (
		<div className="bookDetails">
			<div className={"imageWrapper"}>
				<img src={imageUrlLarge} alt={`The cover for the book „${title}“`}/>
				<Rating rating={+rating_mean}/>
				<span>{rating_count} {rating_count === 1 ? "Bewertung" : "Bewertungen"}</span>
			</div>

			<div className={"detailContent"}>
				<h2>{title}</h2>
				<h3>von {author}</h3>
				<h3>{pubYear}</h3>
				<p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt,
					atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem
					amet.
					Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae
					voluptatem amet. Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor
					explicabo possimus ipsam
					incidunt,
					atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem
					amet.
					Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae
					voluptatem amet.
				</p>
			</div>

			{!!user ? <div className="ratingCTA">
				<h3>Jetzt bewerten</h3>
				<Rating user={user} rating={0} canRate={true} onRate={onRate}/>
			</div> : null}
		</div>
	);
}
