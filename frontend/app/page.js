'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleRight, faAngleLeft, faLock, faColumns } from '@fortawesome/free-solid-svg-icons';
import BookCard from './components/BookCard';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import '@fortawesome/fontawesome-svg-core/styles.css'
import { config } from '@fortawesome/fontawesome-svg-core'
config.autoAddCss = false

export default function Home() {
  const [index, setIndex] = useState(0); // 현재 첫 번째 책의 인덱스
  const [visibleBooks, setVisibleBooks] = useState(4); // 한 번에 보이는 책 개수
  const [books, setBooks] = useState([]);
  const [topic, setTopic] = useState("");
  const router = useRouter();

  // API 호출 - 책 제목 목록 불러오기
  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://123.37.11.58/recommendation');
        const topic = response.data.topic
        const bookTitles = response.data.books.map((title, idx) => ({
          id: idx + 1, // 임시 ID 설정
          title,
          image: `/images/photo${Math.floor(Math.random() * 13) + 1}.png` // 기본 이미지
        }));
        setBooks(bookTitles); // 책 목록 상태 업데이트
        setTopic(topic);
      } catch (error) {
        console.error('Failed to fetch books:', error);
      }
    };

    fetchBooks(); // API 호출 실행
  }, []);

  // 화면 크기에 따라 보이는 책 개수 조정
  useEffect(() => {
    const updateVisibleBooks = () => {
      const width = window.innerWidth;
      if (width >= 1370) setVisibleBooks(4);
      else if (width >= 1024) setVisibleBooks(3);
      else if (width >= 768) setVisibleBooks(2);
      else setVisibleBooks(1);
    };

    window.addEventListener('resize', updateVisibleBooks);
    updateVisibleBooks(); // 초기 화면 크기 설정

    return () => window.removeEventListener('resize', updateVisibleBooks);
  }, []);

  const handleNext = () => {
    if (index + visibleBooks < books.length) {
      setIndex(index + 1);
    }
  };

  const handlePrev = () => {
    if (index > 0) {
      setIndex(index - 1);
    }
  };

  const handleBookClick = (book) => {
    router.push(`/book/${book.title}`);
  };

  return (
    <div style={{display:'flex', flexDirection:'column', textAlign: 'center', marginTop: '40px', position: 'relative' }}>
      <h1 style={{ fontSize: '48px', color: '#4a5a31', paddingTop: '24px', paddingBottom: '8px' }}>금주의 독립서적 큐레이션</h1>
      <h2 style={{ fontsize: '24px', paddingBottom: '16px', fontWeight: 'normal' }}>최근 흐름과 맞닿은 주제들로 엄선한 책을 추천해드려요.</h2>
            
      <div style={{
        display: 'flex',
        justifyContent: 'space-evenly',
        flexDirection: 'row'
      }}><span style={{
        width: '500px', // 고정된 너비 설정
        textAlign: 'center', // 텍스트 가운데 정렬
        fontSize: '32px',
        fontWeight: 'bold',
        margin: '0 auto',
      }}>
        {topic}
      </span></div>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        gap: '20px', // 화살표와 책 사이 간격 조정
        width: '80%',
        margin: '16px auto',
      }}>
        

      <button onClick={handlePrev} disabled={index === 0} style={{
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        fontSize: '24px',
      }}>
        <FontAwesomeIcon icon={faAngleLeft} size="2x" />
      </button>


        <div style={{ 
          display: 'flex',
          justifyContent: 'center',
          gap: '20px',
          overflow: 'hidden', 
          }}
        >
          {books.slice(index, index + visibleBooks).map((book) => (
            <div key={book.id} onClick={() => handleBookClick(book)}>
              <BookCard book={book} />
            </div>
          ))}
        </div>
        <button onClick={handleNext} disabled={index + visibleBooks >= books.length} style={{
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          fontSize: '24px', 
        }}
        >
          <FontAwesomeIcon icon={faAngleRight} size="2x" />
        </button>
      </div>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '24px',
        backgroundColor: 'rgba(74, 90, 49, 0.3)', // 투명도 30% 배경색
        borderRadius: '16px',
        paddingTop: '48px',
        paddingBottom: '16px',
        margin: '20px auto', // 중앙에 배치
        width: '720px',
        textAlign: 'center',
        boxShadow: '0 8px 16px rgba(0, 0, 0, 0.2)', // 그림자 효과
      }}>
        <FontAwesomeIcon icon={faLock} size="2x" style={{ color: 'black' }} />
        <h3 style={{ margin: '16px 0' }}>다양한 인사이트를 담은 이슈별 도서들도 만나보세요!</h3>
        <div>
          <Link href='/purchase'>
            <h2 style={{
              textDecoration: 'none',
              color: '#4a5a31',
              fontSize: '28px',
              fontWeight: 'bold',
            }}>
              결제하기
            </h2>
          </Link>
        </div>
      </div>
    </div>
  );
}
