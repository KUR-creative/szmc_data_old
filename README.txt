 [gui key 매뉴얼]
o	nO-text로 기록
a	All-easy로 기록
h	Half-easy로 기록
n	No-easy로 기록
?	문자가 있는지 없는지 알 수 없음(기본 상태)
!	hasText: 문자가 존재하나 a/h/n 여부는 알 수 없음

f	모드 변경: Full / 원본 높이 / 원본 너비
j	아래로 크게 스크롤
k	위로 크게 스크롤

Enter	이미지에 대한 기록을 확정, 저장하고 다음 이미지로 넘어감.

 키 맵핑(행의 첫번째 키는 이후 키들과 동일하게 인식됨)
o	0
a	1	Space
h	2
n	3

!	[

j	Down
k	Up



 [실행 하는 법]
1. cmd를 실행한다(오른쪽 아래 윈도우 검색창에서 cmd)
2. 적절한 명령어로 NEW_SZMC\ 로 이동
E:
cd NEW_SZMC

3. 
.\NEW_SZMC\szmc\Script\activate.bat
실행
그러면 커맨드라인 앞에 (szmc)가 붙는다.
E:\NEW_SZMC>
(szmc) E:\NEW_SZMC>

4. guy.py 프로그램 실행. 반드시 desc(descendant)로 해야 한다.
(szmc) E:\NEW_SZMC>python gui.py desc


 [데이터베이스 조회하는 법]
gui.py는 NEW_SZMC에 있는 szmc.db에 데이터를 저장한다.
1. szmc.db를 더블클릭하면 디비 브라우저를 켤 수 있다.
2. <SQL 실행> 탭에서 SQL창에 다음을 입력하고 실행 버튼을 누른다.
SELECT * FROM data ORDER BY CAST(id AS INTEGER) DESC
그러면 id의 내림차순으로 배열된 data 테이블을 볼 수 있다.

cf) SELECT * FROM data ORDER BY CAST(id AS INTEGER)   id 오름차순으로 보기
 
 
 [데이터베이스를 수정하는 법]
1. <SQL 실행> 탭에서 조회하여 수정이 필요한 id를 확인하고 복사한다.
2. <데이터 보기> 탭으로 돌아와서 테이블(T)에서 data를 선택한다
3. 원하는 칸을 선택해서 수정하고 '변경사항 저장하기(W)'를 누르면 저장이 된다.

 
 [실수해서 돌아가고 싶을 때]
gui.py는 현재 작업해야할 이미지의 id를 work_state에 저장한다.
1. <SQL 실행> 탭에서 조회하여 수정이 필요한 id를 확인하고 복사한다.
2. <데이터 보기> 탭으로 돌아와서 테이블(T)에서 work_state를 선택한다.
3. id_order는 건드리지 말고, now_id에 1.에서 복사한 id를 붙여넣는다
4. gui.py를 다시 실행한다.


 [유용한 SQL 명령들]

id 내림차순으로 보기
SELECT * FROM data ORDER BY CAST(id AS INTEGER) DESC

id 오름차순으로 보기
SELECT * FROM data ORDER BY CAST(id AS INTEGER)

id로 정렬하여 텍스트가 'O'인 이미지 전부 보기
SELECT * FROM data WHERE text = 'O' ORDER BY CAST(id AS INT)

텍스트가 'O'인 이미지(행) 개수 세기
SELECT count(*) FROM data WHERE text = 'O'

텍스트가 'O'이고 
단부루 메타데이터로 comic이 설정된 이미지들을
id 순서로 나열하여 보기
SELECT * 
FROM data, metadata
WHERE data.id = metadata.id 
  and data.text = 'O' 
  and metadata.comic = 1
ORDER BY CAST(data.id AS INT)

 [dataset directory]

image directory:
    danbooru_raw
    snet_data
    clean_fmd_comics

metadatas:
    dataset


!!!!!! CAUTION !!!!!!
files in dataset are VERY IMPORTANT!
DO NOT REMOVE THIS!

 :NOTE:
for image loading, PIL(Pillow) 6.0.0 needed
for training gan, use cmd: export LD_LIBRARY_PATH=/opt/cuda/lib64  (pacman bug)


