 <������ SQL ��ɵ�>

id�� �����Ͽ� �ؽ�Ʈ�� 'O'�� �̹��� ���� ����
SELECT * FROM data WHERE text = 'O' ORDER BY CAST(id AS INT)

�ؽ�Ʈ�� 'O'�� �̹���(��) ���� ����
SELECT count(*) FROM data WHERE text = 'O'

�ؽ�Ʈ�� 'O'�̰� 
�ܺη� ��Ÿ�����ͷ� comic�� ������ �̹�������
id ������ �����Ͽ� ����
SELECT * 
FROM data, metadata
WHERE data.id = metadata.id 
  and data.text = 'O' 
  and metadata.comic = 1
ORDER BY CAST(data.id AS INT)


 [���� �ϴ� ��]
1. cmd�� �����Ѵ�(������ �Ʒ� ������ �˻�â���� cmd)
2. ������ ��ɾ�� NEW_SZMC\ �� �̵�
E:
cd NEW_SZMC

3. 
.\NEW_SZMC\szmc\Script\activate.bat
����
�׷��� Ŀ�ǵ���� �տ� (szmc)�� �ٴ´�.
E:\NEW_SZMC>
(szmc) E:\NEW_SZMC>

4. guy.py ���α׷� ����. �ݵ�� desc(descendant)�� �ؾ� �Ѵ�.
(szmc) E:\NEW_SZMC>python gui.py desc


 [�����ͺ��̽� ��ȸ�ϴ� ��]
gui.py�� NEW_SZMC�� �ִ� szmc.db�� �����͸� �����Ѵ�.
1. szmc.db�� ����Ŭ���ϸ� ��� �������� �� �� �ִ�.
2. <SQL ����> �ǿ��� SQLâ�� ������ �Է��ϰ� ���� ��ư�� ������.
SELECT * FROM data ORDER BY CAST(id AS INTEGER) DESC
�׷��� id�� ������������ �迭�� data ���̺��� �� �� �ִ�.

cf) SELECT * FROM data ORDER BY CAST(id AS INTEGER)   id ������������ ����
 
 
 [�����ͺ��̽��� �����ϴ� ��]
1. <SQL ����> �ǿ��� ��ȸ�Ͽ� ������ �ʿ��� id�� Ȯ���ϰ� �����Ѵ�.
2. <������ ����> ������ ���ƿͼ� ���̺�(T)���� data�� �����Ѵ�
3. ���ϴ� ĭ�� �����ؼ� �����ϰ� '������� �����ϱ�(W)'�� ������ ������ �ȴ�.

 
 [�Ǽ��ؼ� ���ư��� ���� ��]
gui.py�� ���� �۾��ؾ��� �̹����� id�� work_state�� �����Ѵ�.
1. <SQL ����> �ǿ��� ��ȸ�Ͽ� ������ �ʿ��� id�� Ȯ���ϰ� �����Ѵ�.
2. <������ ����> ������ ���ƿͼ� ���̺�(T)���� work_state�� �����Ѵ�.
3. id_order�� �ǵ帮�� ����, now_id�� 1.���� ������ id�� �ٿ��ִ´�
4. gui.py�� �ٽ� �����Ѵ�.