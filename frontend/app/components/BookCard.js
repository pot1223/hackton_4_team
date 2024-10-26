import Link from 'next/link';
import styles from '../../styles/BookCard.module.css';

const BookCard = ({ book }) => (
  <div className={styles.wrapper}>
    <div className={styles.topic}>{book.topic}</div> {/* 토픽이 이미지 위에 표시되지 않도록 */}
    <Link href={`/book/${book.id}`}>
      <div className={styles.card}>
        <div className={styles.imageWrapper}>
          <img src={book.image} alt={book.title} />
        </div>
        <h3 className={styles.title}>{book.title}</h3> {/* 제목 */}
      </div>
    </Link>
  </div>
);

export default BookCard;