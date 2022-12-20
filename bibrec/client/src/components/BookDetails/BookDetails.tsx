import React from "react";
import RatingStars from "../Books/RatingStars";
import "./BookDetails.scss";
import { User } from "../../App";
import { Book, Rating } from "../../types/types";

interface BookDetailsProps {
	selectedBook: Book;
	onRate: (rating: number) => void;
	user?: User;
	userRating?: Rating;
}

export default function BookDetails({ selectedBook, user, onRate, userRating }: BookDetailsProps) {
	const { image_url_l, book_author, rating_mean, rating_count, book_title, year_of_publication } = selectedBook;

	return (
		<div className="bookDetails">
			<div className={"imageWrapper"}>
				<img src={image_url_l} alt={`The cover for the book „${book_title}“`}/>
				<RatingStars rating={+rating_mean}/>
				<span>{rating_count} {rating_count === 1 ? "Bewertung" : "Bewertungen"}</span>
			</div>

			<div className={"detailContent"}>
				<h2>{book_title}</h2>
				<h3>von {book_author}</h3>
				<h3>{year_of_publication}</h3>
			</div>

			{!!user ? <div className="ratingCTA">
				<h3>{userRating?.book_rating ? "Deine Bewertung" : "Jetzt bewerten"}</h3>
				<RatingStars user={user} rating={userRating?.book_rating ?? 0} canRate={true} onRate={onRate}/>
			</div> : null}
		</div>
	);
}
