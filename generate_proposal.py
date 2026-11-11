import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import os

def create_proposal_docx(filename="PROPOSAL_WORKGUARD.docx"):
    doc = docx.Document()

    # Configure Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    NAVY = RGBColor(10, 37, 64)       # Primary #0A2540
    ACCENT_BLUE = RGBColor(0, 102, 204) # Secondary #0066CC
    DARK_TEXT = RGBColor(34, 34, 34)   # Body #222222
    MUTED_GRAY = RGBColor(100, 100, 100)
    WHITE = RGBColor(255, 255, 255)

    HEX_NAVY = "0A2540"
    HEX_LIGHT_BLUE = "F0F4F8"
    HEX_BORDER = "CCCCCC"

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = DARK_TEXT
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                          f'<w:top w:w="{top}" w:type="dxa"/>'
                          f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                          f'<w:left w:w="{left}" w:type="dxa"/>'
                          f'<w:right w:w="{right}" w:type="dxa"/>'
                          f'</w:tcMar>')
        tcPr.append(tcMar)

    def add_header(title, subtitle=None):
        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_sub = p_sub.add_run("TRƯỜNG ĐẠI HỌC BÁCH KHOA / CÔNG NGHỆ THÔNG TIN\nKHOA KHOA HỌC & KỸ THUẬT MÁY TÍNH\n***")
        run_sub.font.size = Pt(11)
        run_sub.font.bold = True
        run_sub.font.color.rgb = MUTED_GRAY
        p_sub.paragraph_format.space_after = Pt(24)

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_label = p.add_run("BÁO CÁO ĐỀ CƯƠNG ĐỀ TÀI TỐT NGHIỆP / NGHIÊN CỨU\n(PROJECT PROPOSAL)\n\n")
        run_label.font.size = Pt(14)
        run_label.font.bold = True
        run_label.font.color.rgb = ACCENT_BLUE

        run_title = p.add_run("WorkGuard: Automated Fact-Checking and Workslop Detection in LLM-Generated Workplace Documents using Reference-Grounded Evidence Verification\n")
        run_title.font.size = Pt(17)
        run_title.font.bold = True
        run_title.font.color.rgb = NAVY

        run_vi = p.add_run("(Hệ thống tự động kiểm chứng dữ kiện và phát hiện tài liệu doanh nghiệp sáo rỗng do AI tạo ra dựa trên đối soát bằng chứng nguồn)")
        run_vi.font.size = Pt(12)
        run_vi.font.italic = True
        run_vi.font.color.rgb = ACCENT_BLUE
        p.paragraph_format.space_after = Pt(24)

    def add_meta_box():
        table = doc.add_table(rows=3, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        data = [
            ("Lĩnh vực nghiên cứu:", "Trí tuệ nhân tạo (AI), Xử lý ngôn ngữ tự nhiên (NLP), Kiểm định chất lượng tài liệu doanh nghiệp"),
            ("Mã đề tài / Dự án:", "CAPSTONE-2027-WORKGUARD"),
            ("Phương pháp tiếp cận:", "Hybrid: Symbolic Rule Engine + Multilingual Embedding + NLI Cross-Encoder + LLM-as-a-Judge")
        ]

        for i, (label, val) in enumerate(data):
            c1 = table.cell(i, 0)
            c2 = table.cell(i, 1)
            c1.width = Inches(2.2)
            c2.width = Inches(4.3)
            
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(label)
            r1.font.bold = True
            r1.font.size = Pt(10)
            r1.font.color.rgb = NAVY

            p2 = c2.paragraphs[0]
            r2 = p2.add_run(val)
            r2.font.size = Pt(10)
            
            set_cell_background(c1, "F7F9FB")
            set_cell_background(c2, "FFFFFF")
            set_cell_margins(c1, 80, 80, 100, 100)
            set_cell_margins(c2, 80, 80, 100, 100)

        doc.add_paragraph().paragraph_format.space_after = Pt(18)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = ACCENT_BLUE
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = DARK_TEXT
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.bold = True
            r_pre.font.color.rgb = NAVY
        p.add_run(text)
        return p

    def add_callout(text, prefix="LƯU Ý / ĐIỂM QUAN TRỌNG: "):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F0F4F8")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run(prefix)
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY
        r2 = p.add_run(text)
        r2.font.size = Pt(10)
        r2.font.color.rgb = DARK_TEXT
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ---------------- BUILD DOCUMENT ----------------
    add_header("Proposal")
    add_meta_box()

    # 1. TỔNG QUAN & BỐI CẢNH ĐỀ TÀI
    add_heading_1("1. Tổng quan và Bối cảnh Đề tài (Background & Motivation)")
    
    p = doc.add_paragraph()
    p.add_run(
        "Sự bùng nổ của các Mô hình Ngôn ngữ Lớn (LLMs) như GPT-4, Claude, Gemini đã tạo nên một cuộc cách mạng trong năng suất làm việc văn phòng. "
        "Nhân viên trong các doanh nghiệp hiện đại ngày càng phụ thuộc vào AI để soạn thảo các tài liệu công việc quan trọng: văn bản thông báo nội bộ (internal memo), "
        "báo cáo tiến độ (progress report), đề xuất dự án (project proposal) và biên bản cuộc họp (meeting minutes). "
        "Tuy nhiên, sự gia tăng về số lượng văn bản này lại kéo theo một cuộc khủng hoảng mới về chất lượng thông tin trong môi trường doanh nghiệp: "
    )
    r_slop = p.add_run("vấn nạn Workslop.")
    r_slop.font.bold = True

    add_callout(
        "Workslop là thuật ngữ chỉ các sản phẩm tài liệu do Generative AI hỗ trợ tạo ra trông bề ngoài rất bóng bẩy, chuẩn chỉ ngữ pháp, hành văn hoa mỹ, "
        "nhưng thực chất lại rỗng tuếch về mặt nội dung: thiếu số liệu thực chứng, ngụy tạo căn cứ (hallucination), không rõ người chịu trách nhiệm, "
        "không có thời hạn hoàn thành (deadline) và không thể hành động (unactionable). Hậu quả là người đọc (quản lý, đồng nghiệp) phải mất hàng giờ đối chiếu, giải mã hoặc viết lại từ đầu.",
        prefix="ĐỊNH NGHĨA WORKSLOP: "
    )

    doc.add_paragraph(
        "Các công cụ kiểm tra văn bản hiện hành trên thị trường chủ yếu chia thành hai nhánh còn nhiều hạn chế:"
    )
    add_bullet(" Chỉ tập trung vào phân tích phong cách (style, tone) và ngữ pháp cơ bản, hoàn toàn bất lực trước những tuyên bố sai lệch về dữ liệu nghiệp vụ.", bold_prefix="Công cụ Grammar & Style Checker (Grammarly, Word Editor):")
    add_bullet(" Cố gắng dự đoán xác suất văn bản được viết bởi người hay máy bằng Perplexity/Burstiness. Cách tiếp cận này sai lệch về mặt triết lý kinh doanh: doanh nghiệp không cấm nhân viên dùng AI để tăng năng suất; điều doanh nghiệp quan tâm là chất lượng, độ chính xác và tính chịu trách nhiệm của văn bản đầu ra.", bold_prefix="Công cụ AI Detection (Turnitin, GPTZero):")

    doc.add_paragraph(
        "Xuất phát từ khoảng trống công nghệ đó, dự án "
    ).add_run("WorkGuard: Automated Fact-Checking and Workslop Detection in LLM-Generated Workplace Documents using Reference-Grounded Evidence Verification").font.bold = True
    p_last = doc.paragraphs[-1]
    p_last.add_run(
        " được đề xuất nhằm cung cấp một giải pháp toàn diện và thực tiễn: kết hợp kiểm chứng thực chứng (Fact-Checking grounded in source documents) và kiểm định cấu trúc hành động (Actionability & Operational Quality) cho tài liệu văn phòng."
    )

    # 2. MỤC TIÊU NGHIÊN CỨU & ĐÓNG GÓP
    add_heading_1("2. Mục tiêu Nghiên cứu và Phạm vi Đề tài (Research Objectives & Scope)")
    
    add_heading_2("2.1. Mục tiêu Nghiên cứu")
    add_bullet(" Xây dựng mô hình pipeline trích xuất các tuyên bố cốt lõi (Claim Extraction), đối soát với kho tài liệu nguồn tin cậy thông qua kỹ thuật tìm kiếm ngữ nghĩa đa ngôn ngữ (Dense/Sparse Retrieval) và suy luận logic tự nhiên (Natural Language Inference - NLI) để phát hiện mâu thuẫn hoặc số liệu không có căn cứ.", bold_prefix="Mục tiêu 1 (Kiểm chứng Dữ kiện - Fact-Checking):")
    add_bullet(" Thiết lập bộ tiêu chí (Rubric) đánh giá 5 khía cạnh cốt lõi của tài liệu công việc (Mục đích, Tính hành động, Thực chứng, Độ cụ thể, Tính nhất quán). Tự động gắn cờ các câu văn chung chung (generic cliches), trùng lặp (redundancy), và thiếu các trường tác vụ quan trọng (owner, deadline, metric, required decision).", bold_prefix="Mục tiêu 2 (Phát hiện Workslop & Đánh giá Tính hành động):")
    add_bullet(" Cung cấp báo cáo phân tích chi tiết với độ giải thích cao (Explainable AI - XAI), chỉ rõ vị trí câu lỗi trong tài liệu, bằng chứng đối chiếu, phân loại mức độ rủi ro (Risk Level) và gợi ý chỉnh sửa cụ thể (Actionable Suggestions).", bold_prefix="Mục tiêu 3 (Khả năng Giải thích & Tương tác):")
    add_bullet(" Triển khai hệ thống hoàn chỉnh dưới dạng ứng dụng SaaS quy mô nhỏ, có kiến trúc vi dịch vụ (Microservices-ready), hỗ trợ Web UI, REST API và tích hợp thông suốt với các nền tảng văn phòng (Slack, MS Teams, Google Drive).", bold_prefix="Mục tiêu 4 (Xây dựng Sản phẩm Hoàn chỉnh):")

    add_heading_2("2.2. Phạm vi Nghiên cứu (Scope & Deliverables)")
    add_bullet(" Tập trung vào 03 loại văn bản có tần suất sử dụng và rủi ro cao nhất: Báo cáo tiến độ (Project Update/Progress Report), Thông báo nội bộ (Internal Memo), và Đề xuất dự án (Project Proposal).", bold_prefix="Văn bản mục tiêu (Target Documents):")
    add_bullet(" Hỗ trợ trích xuất tự động từ các định dạng văn phòng phổ biến gồm DOCX, PDF, Markdown (.md) và Plain Text (.txt).", bold_prefix="Định dạng đầu vào (Input Formats):")
    add_bullet(" Hỗ trợ song ngữ Tiếng Việt và Tiếng Anh, giải quyết bài toán thiếu hụt công cụ kiểm định chất lượng chuyên sâu cho tiếng Việt văn phòng.", bold_prefix="Ngôn ngữ hỗ trợ (Language Support):")

    # 3. PHƯƠNG PHÁP NGHIÊN CỨU & KIẾN TRÚC HỆ THỐNG
    add_heading_1("3. Phương pháp Tiếp cận và Kiến trúc Kỹ thuật (Methodology & Architecture)")
    
    doc.add_paragraph(
        "Để đạt được hiệu năng cao, chi phí tối ưu và khả năng giải thích minh bạch, WorkGuard áp dụng mô hình kiến trúc phân lớp đa tác tử (Multi-layered Hybrid Architecture), "
        "kết hợp hài hòa giữa các thuật toán tất định (Deterministic Rule Engine) và các mô hình học sâu, LLMs hiện đại."
    )

    # Insert Architecture Image
    image_path = os.path.abspath("WorkGuard.png")
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 1: Sơ đồ Kiến trúc Phân tầng Toàn diện của Hệ thống WorkGuard")
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_GRAY
        p_cap.paragraph_format.space_after = Pt(12)

    add_heading_2("3.1. Các Lớp Kiến trúc Hệ thống (Detailed System Layers)")
    
    add_bullet(" Cung cấp Web Dashboard tương tác cho nhân viên, tích hợp webhook/bot nhận tài liệu trực tiếp từ Slack, Microsoft Teams và kết nối Google Drive nội bộ.", bold_prefix="1. Lớp Tích hợp Người dùng (User & Enterprise Integration Layer):")
    add_bullet(" Xây dựng trên nền tảng FastAPI hiệu năng cao, đóng vai trò Reverse Proxy, xác thực người dùng bằng JWT, kiểm soát truy cập theo vai trò (RBAC: Admin, Reviewer, User), Rate Limiting và ghi vết kiểm toán (Audit Logging).", bold_prefix="2. Lớp Cổng Giao diện (API Gateway Layer):")
    add_bullet(" Module chuyên trách bóc tách tài liệu (python-docx, PyMuPDF, markdown-it-py), chuẩn hóa văn bản, trích xuất cấu trúc đề mục (headings, paragraphs, bullet points, tables), phân đoạn ngữ nghĩa (chunking) và đẩy file gốc lên MinIO/S3.", bold_prefix="3. Lớp Tiếp nhận Tài liệu (Document Ingestion Layer):")
    add_bullet(" Hệ quản trị Cơ sở dữ liệu quan hệ PostgreSQL quản lý siêu dữ liệu (metadata), cây cấu trúc văn bản, kết quả phân tích (findings, claims, runs); MinIO Object Storage lưu trữ tài liệu gốc có mã hóa.", bold_prefix="4. Lớp Lưu trữ Tài liệu (Document Store Layer):")
    add_bullet(" Đóng vai trò 'nhạc trưởng', sử dụng Celery Worker cùng Redis Message Broker để quản lý hàng đợi tác vụ bất đồng bộ, tự động nhận diện loại văn bản và áp dụng Rubric tương ứng.", bold_prefix="5. Lớp Điều phối Phân tích (Analysis Orchestrator Layer):")
    add_bullet(" Trái tim phân tích của WorkGuard, vận hành song song 4 cơ chế độc lập (chi tiết tại mục 3.2).", bold_prefix="6. Lớp Động cơ Phân tích Chất lượng (Quality Analysis Engine Layer):")
    add_bullet(" Tích hợp mô hình ngôn ngữ lớn Qwen3-8B (hoạt động on-premise hoặc API fallback), mô hình nhúng ngữ nghĩa đa ngôn ngữ BAAI/bge-m3, và mô hình cross-encoder NLI.", bold_prefix="7. Lớp Trí tuệ Nhân tạo & Mô hình (AI / Model Layer):")
    add_bullet(" Tổng hợp kết quả từ 4 phân hệ, áp dụng ma trận trọng số, tính toán Điểm Chất lượng Tổng thể (Quality Score: 0-100) và xếp loại Rủi ro (Ready, Needs Revision, High Risk).", bold_prefix="8. Lớp Tổng hợp Kết quả (Result Aggregation Layer):")
    add_bullet(" Xuất báo cáo đa định dạng (PDF/JSON), hiển thị bảng điều khiển trực quan với các câu trích dẫn kèm bằng chứng đối sánh, sẵn sàng trả lời qua API Webhook.", bold_prefix="9. Lớp Báo cáo & Xuất bản (Reporting & Integration Layer):")

    add_heading_2("3.2. Cơ chế Hoạt động của 4 Phân hệ Đánh giá Cốt lõi")
    
    # Table of 4 Engines
    table_eng = doc.add_table(rows=5, cols=3)
    table_eng.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_eng.autofit = False

    headers = ["Phân hệ Phân tích", "Kỹ thuật / Công nghệ Áp dụng", "Mục tiêu Phát hiện & Kiểm chứng"]
    for j, h in enumerate(headers):
        cell = table_eng.cell(0, j)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = WHITE

    engine_data = [
        ("Rule Engine (Kiểm tra Quy tắc)", "Regex, Spacy POS Tagging, Named Entity Recognition (NER), Heuristics", "Phát hiện nhanh các lỗi cấu trúc: thiếu người chịu trách nhiệm (missing owner), thiếu thời hạn (missing deadline), hành động mơ hồ (vague actions), số liệu không có nguồn gốc."),
        ("LLM Rubric Scorer (Chấm điểm Rubric)", "Qwen3-8B / LLM API + Structured Output (JSON Schema)", "Đánh giá định tính sâu theo 5 tiêu chí Rubric doanh nghiệp: Độ rõ ràng mục tiêu, Tính khả thi thực tế, Chất lượng căn cứ, Độ súc tích và Tính nhất quán nghiệp vụ."),
        ("Claim & Evidence Verifier (Kiểm chứng Bằng chứng)", "BAAI/bge-m3 Embedding + Qdrant Vector DB + Cross-Encoder NLI", "Trích xuất các mệnh đề dữ kiện (claims), tìm kiếm đoạn văn chứng cứ (evidence retrieval) từ tài liệu nguồn, kiểm tra quan hệ suy diễn logic: Supported, Partially Supported, Unsupported, Contradicted."),
        ("Similarity & Redundancy Detector", "Sentence-Transformers, Cosine Similarity, N-gram Overlap", "Phát hiện sự trùng lặp ý tưởng giữa các phần trong văn bản, phát hiện các đoạn văn sáo rỗng (filler text/cliches) thường thấy trong văn bản do AI sinh ra tự động.")
    ]

    col_widths = [Inches(1.8), Inches(2.0), Inches(2.7)]
    for i, row in enumerate(engine_data):
        for j, val in enumerate(row):
            cell = table_eng.cell(i+1, j)
            cell.width = col_widths[j]
            bg = "F9FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. BỘ TIÊU CHÍ RUBRIC ĐÁNH GIÁ TÀI LIỆU
    add_heading_1("4. Bộ Tiêu chuẩn Rubric Đánh giá Văn bản Doanh nghiệp (WorkGuard Rubric)")
    doc.add_paragraph(
        "Hệ thống không đánh giá cảm tính mà dựa trên khung chuẩn Rubric gồm 5 chiều đo lường cốt lõi, được lượng hóa thành thang điểm cụ thể:"
    )

    rubrics = [
        ("1. Purpose Clarity (Độ rõ ràng về mục đích):", " Tài liệu phải nêu rõ lý do tồn tại, đối tượng hướng tới và kết quả kỳ vọng. Phát hiện các tài liệu chỉ mang tính chất 'cập nhật tình hình' chung chung mà không phục vụ mục đích kinh doanh nào."),
        ("2. Actionability (Tính hành động & Quyết định):", " Mọi mục hành động (action item) bắt buộc phải có chủ thể (Owner), mốc thời hạn (Deadline), chỉ số đo lường (Metric) và thẩm quyền phê duyệt rõ ràng. Nghiêm cấm các phát biểu mơ hồ như 'Team sẽ tiếp tục nỗ lực cải thiện'."),
        ("3. Evidence & Grounding (Căn cứ & Tính thực chứng):", " Mọi tuyên bố mang tính khẳng định (ví dụ: 'Doanh thu tăng trưởng mạnh', 'Khách hàng rất hài lòng') đều phải gắn liền với nguồn dữ liệu tham chiếu, số liệu kiểm chứng từ hệ thống hoặc báo cáo đính kèm."),
        ("4. Specificity & Anti-slop (Độ cụ thể & Chống sáo rỗng):", " Khấu trừ điểm nghiêm khắc đối với các đoạn văn dùng thuật ngữ sáo rỗng (corporate buzzwords/filler), lặp ý vô nghĩa hoặc dài dòng nhằm đối phó dung lượng."),
        ("5. Consistency & Verifiability (Tính nhất quán & Khả năng kiểm tra):", " Đảm bảo tính logic nội tại giữa các phần (ví dụ: mâu thuẫn giữa tóm tắt điều hành và bảng biểu chi tiết) và sự phù hợp với các tài liệu nền tảng của tổ chức.")
    ]

    for title, desc in rubrics:
        add_bullet(desc, bold_prefix=title)

    # Thang điểm và phân loại rủi ro
    add_heading_2("4.1. Công thức Tính Điểm và Phân loại Rủi ro (Scoring & Risk Matrix)")
    doc.add_paragraph(
        "Điểm chất lượng văn bản (WorkGuard Quality Score - WQS) được tính theo công thức trung bình có trọng số:"
    )
    p_form = doc.add_paragraph()
    p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_form = p_form.add_run("WQS = Σ (w_i × S_i)  với  Σ w_i = 1.0  (i = 1..5)")
    r_form.font.bold = True
    r_form.font.size = Pt(11)
    r_form.font.color.rgb = NAVY

    doc.add_paragraph(
        "Dựa trên WQS, tài liệu được phân thành 3 cấp độ rủi ro phục vụ tự động hóa quy trình phê duyệt:"
    )
    add_bullet(" Tài liệu đạt chuẩn xuất sắc, đầy đủ căn cứ, sẵn sàng lưu hành hoặc trình cấp quản lý phê duyệt.", bold_prefix="Điểm 80 - 100 [READY - Sẵn sàng]:")
    add_bullet(" Tài liệu còn thiếu sót một số trường tác vụ (thiếu deadline, một số tuyên bố cần bổ sung số liệu), hệ thống trả về đề xuất để tác giả hoàn thiện.", bold_prefix="Điểm 50 - 79 [NEEDS REVISION - Cần chỉnh sửa]:")
    add_bullet(" Tài liệu chứa thông tin mâu thuẫn nghiêm trọng với tài liệu nguồn, sai lệch số liệu, hoàn toàn sáo rỗng hoặc thiếu tính khả thi; bị chặn lưu hành tự động.", bold_prefix="Điểm 0 - 49 [HIGH RISK - Rủi ro cao]:")

    # 5. HIỆU QUẢ DỰ KIẾN & TÍNH KHẢ THI
    add_heading_1("5. Hiệu quả Đề tài và Tính Khả thi (Feasibility & Expected Impact)")
    
    add_heading_2("5.1. Đóng góp về mặt Khoa học và Công nghệ")
    add_bullet(" Đề xuất phương pháp luận mới trong việc kiểm định chất lượng nội dung do AI tạo ra, chuyển dịch trọng tâm từ 'phát hiện AI' sang 'đánh giá giá trị nghiệp vụ thực tế'.", bold_prefix="Phương pháp luận mới:")
    add_bullet(" Ứng dụng thành công kỹ thuật kết hợp giữa NLI (Natural Language Inference) và Dense Multilingual Retrieval (BGE-M3) để giải quyết bài toán Fact-checking trong tài liệu văn phòng Tiếng Việt.", bold_prefix="Làm chủ công nghệ NLP/LLM:")

    add_heading_2("5.2. Hiệu quả Ứng dụng Thực tiễn trong Doanh nghiệp")
    add_bullet(" Cắt giảm 60 - 80% thời gian của cấp quản lý trong việc đọc, rà soát và kiểm chứng tính xác thực của các báo cáo dự án.", bold_prefix="Tiết kiệm thời gian rà soát:")
    add_bullet(" Ngăn chặn kịp thời các rủi ro vận hành do nhân viên ra quyết định dựa trên những cam kết 'ảo', số liệu không có căn cứ do LLMs tự bịa ra.", bold_prefix="Giảm thiểu rủi ro vận hành:")
    add_bullet(" Giúp nhân viên tự hoàn thiện kỹ năng viết báo cáo thông qua các gợi ý chỉnh sửa cụ thể, trực quan.", bold_prefix="Nâng cao văn hóa làm việc:")

    add_heading_2("5.3. Tính Khả thi Kỹ thuật & Hạ tầng (Feasibility Analysis)")
    add_bullet(" Đề tài tận dụng các thư viện mã nguồn mở hàng đầu (FastAPI, Celery, Spacy, BGE-M3, PyTorch), có cộng đồng lớn và độ ổn định cao.", bold_prefix="Nền tảng công nghệ sẵn sàng:")
    add_bullet(" Sử dụng mô hình nguồn mở tối ưu (Qwen3-8B hoặc Qwen2.5-7B) kết hợp lượng tử hóa (Quantization 4-bit/8-bit), hoàn toàn có khả năng chạy trên GPU tiêu chuẩn (Kaggle T4/P100, RTX 3090/4090) hoặc thông qua API chi phí thấp.", bold_prefix="Chi phí tính toán hợp lý:")

    # 6. KẾT LUẬN & KIẾN NGHỊ
    add_heading_1("6. Kết luận và Đề xuất (Conclusion & Recommendation)")
    doc.add_paragraph(
        "Đề tài "
    ).add_run("WorkGuard: Automated Fact-Checking and Workslop Detection in LLM-Generated Workplace Documents using Reference-Grounded Evidence Verification").font.bold = True
    p_end = doc.paragraphs[-1]
    p_end.add_run(
        " giải quyết trực diện một vấn nạn nhức nhối và cấp thiết nhất của kỷ nguyên Generative AI trong doanh nghiệp. "
        "Với mục tiêu rõ ràng, cơ sở lý thuyết vững chắc, kiến trúc kỹ thuật hiện đại và phương pháp tiếp cận khả thi, "
        "nhóm nghiên cứu tin tưởng đề tài sẽ mang lại một sản phẩm có tính ứng dụng thực tiễn cao, đóng góp thiết thực cho cộng đồng nghiên cứu và ứng dụng CNTT."
    )

    # Signature block
    doc.add_paragraph().paragraph_format.space_after = Pt(24)
    table_sig = doc.add_table(rows=1, cols=2)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_sig1 = table_sig.cell(0, 0)
    c_sig2 = table_sig.cell(0, 1)
    c_sig1.width = Inches(3.2)
    c_sig2.width = Inches(3.3)

    p_s1 = c_sig1.paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s1 = p_s1.add_run("GIẢNG VIÊN HƯỚNG DẪN\n(Ký và ghi rõ họ tên)\n\n\n\n\n...................................................")
    r_s1.font.size = Pt(11)
    r_s1.font.bold = True
    r_s1.font.color.rgb = DARK_TEXT

    p_s2 = c_sig2.paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s2 = p_s2.add_run("SINH VIÊN / NHÓM THỰC HIỆN\n(Ký và ghi rõ họ tên)\n\n\n\n\n...................................................")
    r_s2.font.size = Pt(11)
    r_s2.font.bold = True
    r_s2.font.color.rgb = DARK_TEXT

    doc.save(filename)
    print(f"File saved successfully as {filename}")

if __name__ == "__main__":
    create_proposal_docx("PROPOSAL_WORKGUARD.docx")
