'use client';

import Header from '../../components/Header';
import { useEffect, useState } from 'react';
import styles from '../../../styles/BookDetail.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBookOpen } from '@fortawesome/free-solid-svg-icons';


const bookDetails = {
  '1': {
    title: '거절을 믿듯 선의 또 한 믿으며',
    author: '김한윤',
    genre: '국내도서 > 시/에세이',
    summary: '당신의 여기까지와 거절과 선의를 믿으며 살아가는 삶의 태도를 이야기합니다.',
    authorInfo: '저자는 올 봄에 에세이로 데뷔했으며, 거절과 믿음의 가치에 대해 글을 씁니다.',
    insideBook: '이밤 저녁은 길게 느껴졌다. 발가락이 로켓이 올라왔다 (p.73-75).',
    image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg'
  },
  '2': { 
    title: '채식주의자',
    author: '한강',
    genre: '국내도서 > 소설',
    summary: '채식주의자가 된 한 여성을 중심으로 벌어지는 사건과 가족의 갈등을 다룹니다.',
    authorInfo: '한강은 한국 문학의 대표적 작가로, 여러 문학상을 수상하였습니다.',
    insideBook: '나는 나뭇잎을 보고 그 맛을 기억했다. (p.52).',
    image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg'
  },
};

const BookDetail = ({ params }) => {
  const { id } = params;
  const [book, setBook] = useState(null);

  useEffect(() => {
    setBook(bookDetails[id]);
  }, [id]);

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
      <h1 style={{ fontSize: '24px', margin: 0 }}>도서 정보를 찾을 수 없습니다.</h1>
    </div>
  );

  return (
    <div className={styles.detailContainer}>
      <div className={styles.textContainer}>
        <h1 className={styles.bookTitle}>{book.title}</h1>

        <div className={styles.textRow}>
          <strong>저자</strong> <span>{book.author}</span>
        </div>
        <div className={styles.textRow}>
          <strong>장르</strong> <span>{book.genre}</span>
        </div>
        <div className={styles.textRow}>
          <strong>줄거리</strong> <span>{book.summary}</span>
        </div>
        <div className={styles.textRow}>
          <strong>작가 소개</strong> <span>{book.authorInfo}</span>
        </div>
        <div className={styles.textRow}>
          <strong>책 속으로</strong> <span>{book.insideBook}</span>
        </div>
      </div>

      <div className={styles.imageContainer}>
        <img src={book.image} alt={book.title} />
      </div>
    </div>
  );
};

export default BookDetail;