'use client';

import Header from '../../components/Header';
import { useEffect, useState } from 'react';
import styles from '../../../styles/BookDetail.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBookOpen } from '@fortawesome/free-solid-svg-icons';
import { useParams } from 'next/navigation';
import axios from 'axios';


export default function BookDetail() {
  const { title } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    if (!title) return; // title이 없으면 실행 안 함
    const fetchBookInfo = async () => {
      try {
        const response = await axios.get(
          `http://123.37.11.58:80/book_info?title=${title}`
        );
        setBook(response.data); // API로부터 받은 책 정보 저장
      } catch (error) {
        console.error('도서 정보를 가져오는 데 실패했습니다:', error);
      }
    };

    fetchBookInfo(); // API 호출 실행
  }, [title]);

  if (!book) return (
    <div style={{ 
      position: 'absolute', 
      left: '50%', 
      top: '50%', 
      transform: 'translate(-50%, -50%)', 
      textAlign: 'center' 
    }}>
      <FontAwesomeIcon 
        icon={faBookOpen} 
        style={{ fontSize: '100px', marginBottom: '16px', color: '#4a5a31', opacity: '0.5' }} 
      />
      <h1 style={{ fontSize: '24px', margin: 0 }}>Loading...</h1>
    </div>
  );

  return (
    <div className={styles.detailContainer}>
      <div className={styles.textContainer}>
        <h1 className={styles.bookTitle}>{book.title}</h1>

        <div className={styles.textRow}>
          <strong>저자</strong> <span>{book?.author}</span>
        </div>
        <div className={styles.textRow}>
          <strong>장르</strong> <span>{book?.genre}</span>
        </div>
        <div className={styles.textRow}>
          <strong>줄거리</strong> <span>{book?.summary}</span>
        </div>
        <div className={styles.textRow}>
          <strong>작가 소개</strong> <span>{book?.author_intro}</span>
        </div>
        <div className={styles.textRow}>
          <strong>책 속으로</strong> <span>{book?.excerpt}</span>
        </div>
      </div>

      <div className={styles.imageContainer}>
        <img src={'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg'} alt={book.title} />
      </div>
    </div>
  );
};