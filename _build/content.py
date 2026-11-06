# -*- coding: utf-8 -*-
"""All page copy for EditPDF. Edit text here, then run:  python build.py"""

HERO_LINE = ("Everything you need to work with PDFs. Fast, free, and right in your browser — "
             "no account or software installation needed.")

TOOLS = [
 dict(slug="compress-pdf", key="compress", name="Compress PDF", cat="Convert & Compress", color="icon-coral",
  icon='<path d="M8 3H5a2 2 0 0 0-2 2v3m13-5h3a2 2 0 0 1 2 2v3M3 16v3a2 2 0 0 0 2 2h3m13-5v3a2 2 0 0 1-2 2h-3M8 8l4 4 4-4M12 12V5M8 16h8"/>',
  card="Reduce PDF file size for easy sharing.", cta="Compress file",
  title="Compress PDF Online Free – Reduce PDF Size | EditPDF",
  desc="Compress a PDF online for free. Shrink scanned or image-heavy PDFs for email and uploads. Runs in your browser, so your file is never uploaded.",
  h1="Compress PDF Online — Free", lead="Make a large PDF smaller so it is easier to email, upload or store. Choose a compression level, and the work happens right in your browser.",
  libs=["pdfjs","jspdf"],
  steps=[("Choose your PDF","Click the box or drag a PDF into it. The file stays on your device."),
         ("Pick a compression level","Balanced works for most files. Choose Strong when you need the smallest size."),
         ("Download the result","The new PDF downloads automatically, and the page shows how much smaller it is.")],
  feats=[("Works best on scans and photos","Scanned documents and image-heavy PDFs usually shrink the most because each page is re-saved as an optimized image."),
         ("Three compression levels","Trade file size against sharpness: strong, balanced or high quality."),
         ("Private by design","Your PDF is processed by your own browser. EditPDF does not receive a copy."),
         ("Honest results","The page tells you the before and after size, so you can keep whichever file is better.")],
  limits="<strong>Good to know:</strong> this tool re-draws every page as an image. That can make scanned or photo-heavy PDFs much smaller, but the text in the new file is no longer selectable or searchable. If the result is larger than the original, keep the original. PDFs that are mostly text are often already small and may not shrink.",
  faq=[("Why is my compressed PDF not searchable?","The tool converts each page to a compressed image to reduce size. Images do not contain selectable text. If you need searchable text, keep the original PDF or run OCR software afterwards."),
       ("Will it always make my PDF smaller?","No. Text-based PDFs are already compact and can come out larger. The page shows the new size after processing so you can compare and keep the better file."),
       ("Is my PDF uploaded to a server?","No. Compression runs in your browser using JavaScript libraries. Your file is not sent to EditPDF."),
       ("How do I get the smallest possible size?","Choose Strong compression. Pages are rendered at a lower resolution and saved with higher JPEG compression, so quality drops a little."),
       ("Is there a file size limit?","There is no fixed limit, but very large PDFs use a lot of memory. If your browser struggles, try a smaller file or a computer with more memory.")],
  related=["merge-pdf","split-pdf","image-to-pdf"], guide="how-to-compress-a-pdf",
  about="Compressing a PDF means reducing the number of bytes it takes up so it opens faster and fits within email or upload limits. The biggest savings come from images: a scan of a ten-page contract can be tens of megabytes because every page is a full-resolution photo."),
 dict(slug="image-to-pdf", key="image", name="Image to PDF", cat="Convert & Compress", color="icon-blue",
  icon='<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="9" cy="9" r="1.5"/><path d="m20 15-5-5L5 20"/>',
  card="Turn JPG, PNG and WebP images into a PDF.", cta="Convert images",
  title="JPG to PDF Converter Free – Images to PDF | EditPDF",
  desc="Convert JPG, PNG and WebP images to one PDF online for free. Reorder pages, pick A4 or Letter. No sign-up, and your images never leave your device.",
  h1="Image to PDF Converter — JPG, PNG & WebP", lead="Combine one or more pictures into a single PDF. Set the page order, choose a page size, and download — all in your browser.",
  libs=["jspdf"],
  steps=[("Add your images","Select JPG, PNG or WebP files, or drag them in. You can add more than one batch."),
         ("Set order and page size","Use the arrows to reorder pages, then choose A4, US Letter or fit-to-image."),
         ("Create and download","Click Create PDF. Your document is built on your device and downloads straight away.")],
  feats=[("Multiple images, one PDF","Turn a stack of photos or screenshots into a single multi-page document."),
         ("Reorder before you convert","Move pages up or down so the PDF is in exactly the order you want."),
         ("A4, Letter or exact size","Place each image on a standard page, or make every page match its image."),
         ("No upload, no account","Images are read and converted locally, so private photos stay private.")],
  limits="<strong>Good to know:</strong> WebP images are converted to JPEG before they are placed in the PDF, and transparent areas become white. Very large photos can make large PDFs; use the Compress PDF tool afterwards if you need a smaller file.",
  faq=[("Which image formats are supported?","JPG/JPEG, PNG and WebP."),
       ("Can I put several images into one PDF?","Yes. Add as many images as your device can handle and reorder them with the arrows. Each image becomes its own page."),
       ("Will my images be uploaded?","No. They are read by your browser and the PDF is created locally."),
       ("What does 'fit page to each image' do?","Each PDF page is sized to match its image, with no margins. Choose A4 or Letter if you want standard paper-size pages."),
       ("How can I make the PDF smaller?","Resize large photos before converting, or run the finished file through the Compress PDF tool.")],
  related=["merge-pdf","compress-pdf","rotate-pdf"], guide="how-to-convert-images-to-pdf",
  about="Turning pictures into a PDF is useful for scanned receipts, signed forms photographed with a phone, school assignments and portfolios. A PDF keeps your pages in a fixed order and opens the same way on every device."),
 dict(slug="merge-pdf", key="merge", name="Merge PDF", cat="Organize PDF", color="icon-purple",
  icon='<path d="M8 4H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-3M9 2h6l5 5v5M15 2v5h5M8 12h8m-4-4v8"/>',
  card="Combine multiple PDFs into one file.", cta="Merge files",
  title="Merge PDF Files Online Free – Combine PDFs | EditPDF",
  desc="Merge PDF files into one document online for free. Add files, set the order, and download. Works in your browser — no upload, no account.",
  h1="Merge PDF Files Online — Free", lead="Combine two or more PDFs into one document in the order you choose. Nothing is uploaded, because the merge happens in your browser.",
  libs=["pdflib"],
  steps=[("Add two or more PDFs","Select your files or drag them into the box. Add more at any time."),
         ("Arrange the order","Use the arrows to move files up or down. The top file comes first."),
         ("Merge and download","Click Merge PDFs. Your combined file downloads automatically.")],
  feats=[("Keeps pages as they are","Pages are copied into the new file, so text stays selectable and layouts do not change."),
         ("Full control of the order","Reorder files before merging instead of fixing the order afterwards."),
         ("Many files at once","Combine contracts, invoices, chapters or scans in one go."),
         ("Private and free","Files never leave your device and there is no sign-up.")],
  limits="<strong>Good to know:</strong> password-protected or damaged PDFs cannot be merged. Remove the password in the program that created the file first. Very large files can take a while on older devices.",
  faq=[("How do I merge PDF files for free?","Add your PDFs, put them in the order you want with the arrows, and click Merge PDFs. The combined file downloads to your device."),
       ("Is the text still selectable after merging?","Yes. Pages are copied as they are, not converted to images."),
       ("Can I merge password-protected PDFs?","Not directly. Remove the password using the original program, then merge the unlocked files."),
       ("Are my documents uploaded?","No. Merging runs in your browser with a JavaScript library, so your files stay on your device."),
       ("Is there a limit on the number of files?","There is no fixed limit. The practical limit is your device's memory.")],
  related=["split-pdf","compress-pdf","rotate-pdf"], guide="how-to-merge-pdf-files",
  about="Merging PDFs saves you from sending many separate attachments. Typical uses are job applications (CV plus certificates), invoices for one month, or chapters of a report prepared by different people."),
 dict(slug="split-pdf", key="split", name="Split PDF", cat="Organize PDF", color="icon-green",
  icon='<path d="M7 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h5M7 3h7l5 5v3M14 3v5h5M14 14l7 7m0-7-7 7"/>',
  card="Extract selected pages into a new PDF.", cta="Split document",
  title="Split PDF Online Free – Extract Pages from PDF | EditPDF",
  desc="Split a PDF or extract specific pages online for free. Type page numbers like 1,3-5 and download a new PDF. No upload, no account.",
  h1="Split PDF & Extract Pages — Free", lead="Pull the pages you need out of a PDF and save them as a new file. Type the page numbers and the tool does the rest in your browser.",
  libs=["pdflib"],
  steps=[("Choose a PDF","Select or drag in the document you want to split."),
         ("Enter the pages","Type page numbers and ranges, for example 1,3-5 to keep pages 1, 3, 4 and 5."),
         ("Download the new PDF","Click Extract pages. The new, shorter PDF downloads immediately.")],
  feats=[("Flexible page selection","Use single pages, ranges, or both together."),
         ("Original quality","Selected pages are copied unchanged, so text and images stay sharp."),
         ("Good for sharing part of a file","Send one chapter or one signed page instead of a whole document."),
         ("Private","Your PDF is processed locally in your browser.")],
  limits="<strong>Good to know:</strong> the tool creates one new PDF from the pages you list. To get several separate files, run it once for each set of pages. Password-protected PDFs cannot be processed.",
  faq=[("How do I extract pages from a PDF?","Upload the file, type the pages you want, such as 2-4, and click Extract pages. A new PDF containing only those pages is downloaded."),
       ("How do I write the page range?","Separate items with commas and use a hyphen for ranges: 1,3-5,8 keeps pages 1, 3, 4, 5 and 8. Page numbers start at 1."),
       ("Does splitting reduce quality?","No. Pages are copied directly, so there is no quality loss."),
       ("Can I split a PDF into many files at once?","Not in one step. Run the tool once for each group of pages you need."),
       ("Is my file uploaded anywhere?","No. Everything happens in your browser.")],
  related=["merge-pdf","rotate-pdf","pdf-page-counter"], guide=None,
  about="Splitting a PDF is helpful when you only need part of a long document: a single invoice from a statement bundle, one chapter from a manual, or the signature page of a contract."),
 dict(slug="rotate-pdf", key="rotate", name="Rotate PDF", cat="Organize PDF", color="icon-orange",
  icon='<path d="M20 7v5h-5M4 17v-5h5M5.6 9A7 7 0 0 1 18 6l2 6M4 12l2 6a7 7 0 0 0 12.4-3"/>',
  card="Fix pages that are sideways or upside down.", cta="Rotate pages",
  title="Rotate PDF Online Free – Fix Sideways Pages | EditPDF",
  desc="Rotate PDF pages 90, 180 or 270 degrees online for free and save the result. Fix sideways or upside-down scans in your browser. No upload.",
  h1="Rotate PDF Online — Free", lead="Fix a sideways or upside-down document. Pick an angle, rotate every page, and download the corrected PDF.",
  libs=["pdflib"],
  steps=[("Choose a PDF","Select the document that needs rotating."),
         ("Pick an angle","Choose 90° clockwise, 180°, or 270° clockwise."),
         ("Download","Click Rotate PDF and save the corrected file.")],
  feats=[("Permanent rotation","The new PDF opens with the correct orientation in any viewer."),
         ("No quality loss","Pages are rotated, not re-rendered, so text stays sharp and selectable."),
         ("Fast","Even long documents rotate in moments on a modern device."),
         ("Private","The file stays on your device.")],
  limits="<strong>Good to know:</strong> this tool rotates every page by the same angle. To rotate only some pages, split them out first, rotate, then merge everything back together.",
  faq=[("How do I rotate a PDF and save it?","Choose your PDF, pick the angle, and click Rotate PDF. The rotated file downloads and keeps the new orientation."),
       ("Can I rotate just one page?","This tool rotates all pages. To rotate a single page, extract it with Split PDF, rotate it, and merge it back with Merge PDF."),
       ("Does rotating change the quality?","No. The rotation is stored in the PDF page settings; the content is not re-compressed."),
       ("Which direction is 90°?","Clockwise. Use 270° for a quarter-turn counter-clockwise."),
       ("Are my files uploaded?","No. The tool runs entirely in your browser.")],
  related=["split-pdf","merge-pdf","compress-pdf"], guide=None,
  about="Scanners and phone cameras often save pages sideways. Rotating the PDF once fixes the orientation for everyone you share it with, instead of each person rotating the view by hand."),
 dict(slug="pdf-page-counter", key="pages", name="PDF Page Counter", cat="PDF Info", color="icon-pink",
  icon='<path d="M7 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-3M7 3h7l5 5v3M14 3v5h5M8 13h5M8 17h3"/>',
  card="Check how many pages your PDF contains.", cta="Count pages",
  title="PDF Page Counter – Count Pages in a PDF Free | EditPDF",
  desc="Count the pages in any PDF instantly and free. Find the page total and file size in your browser. No upload, no sign-up.",
  h1="PDF Page Counter — Count Pages in a PDF", lead="Find out how many pages a PDF has in a second. Your file is read in your browser and never uploaded.",
  libs=["pdflib"],
  steps=[("Choose a PDF","Select the document or drag it into the box."),
         ("Click Count pages","The tool reads the file's page list."),
         ("See the result","The page count and file size are shown right away.")],
  feats=[("Instant answer","Get the total number of pages without opening a big file in a viewer."),
         ("Also shows file size","Handy when you need to check upload limits."),
         ("Nothing is stored","The file is read locally and discarded when you close the page."),
         ("Free forever","No account and no usage limits.")],
  limits="<strong>Good to know:</strong> password-protected PDFs cannot be read. For more details such as title, author and page size, use the <a href=\"/pdf-info/\">PDF Info</a> tool.",
  faq=[("How do I count pages in a PDF online?","Choose the file and click Count pages. The total is shown on screen."),
       ("Does it work on large PDFs?","Yes, as far as your device's memory allows. Only the page structure is read."),
       ("Is the PDF uploaded?","No. The count is calculated in your browser."),
       ("Why do I get an error?","The file may be password-protected or damaged. Remove the password and try again."),
       ("Can I see more details about the file?","Yes — use the PDF Info tool to see title, author, page size and dates.")],
  related=["pdf-info","split-pdf","merge-pdf"], guide=None,
  about="Knowing the page count helps when a form limits submissions to a number of pages, when you are estimating print costs, or when you need to choose page ranges for splitting."),
 dict(slug="pdf-info", key="info", name="PDF Info", cat="PDF Info", color="icon-slate",
  icon='<circle cx="12" cy="12" r="9"/><path d="M12 11v5m0-8h.01"/>',
  card="View page count, size and document properties.", cta="Inspect PDF",
  title="PDF Info Viewer – Check PDF Properties Online | EditPDF",
  desc="See a PDF's page count, page size, title, author, creator and dates online for free. Private — the file is read in your browser, not uploaded.",
  h1="PDF Info Viewer — Check PDF Properties", lead="View the page count, page size and document properties of a PDF. Everything is read locally in your browser.",
  libs=["pdflib"],
  steps=[("Choose a PDF","Select a file or drag it into the box."),
         ("Click Show information","The tool reads the document's properties."),
         ("Review the details","See size, pages, title, author, creator, producer and dates.")],
  feats=[("Document properties at a glance","Title, author, subject, creator and producer if the file contains them."),
         ("Dates","Creation and modification dates stored in the file."),
         ("Page size","The size of the first page in PDF points."),
         ("Private","No upload. The file is read in your browser.")],
  limits="<strong>Good to know:</strong> many PDFs leave some fields empty, and those show as “Not specified”. Properties are stored by the program that made the file and may not always be accurate.",
  faq=[("What information does the tool show?","File name and size, page count, page size, and the title, author, subject, creator, producer, creation date and modified date when they are present."),
       ("Why are some fields empty?","The program that created the PDF did not store them. That is common."),
       ("Is it safe for confidential files?","The file is read in your browser and is not uploaded to EditPDF. Avoid shared or public computers for sensitive documents."),
       ("Can I edit the properties?","Not in this tool. It is a viewer only."),
       ("What is a PDF point?","A unit equal to 1/72 inch. A standard A4 page is about 595 × 842 points.")],
  related=["pdf-page-counter","split-pdf","compress-pdf"], guide=None,
  about="PDF properties show where a file came from and how it was produced. They are useful for checking page size before printing, confirming which version of a document you have, or seeing which program created a file."),
]

GUIDES = [
 dict(slug="how-to-merge-pdf-files", title="How to Merge PDF Files Into One (Free, No Software) | EditPDF",
  desc="Step-by-step guide to combining several PDFs into one file for free. Includes tips on order, file size and common problems.",
  h1="How to Merge PDF Files Into One", lead="Combining PDFs takes about a minute and needs no software. Here is how to do it, and how to avoid the usual problems.",
  card="A quick guide to combining PDFs.", tool="merge-pdf", tool_cta="Merge PDF files now",
  body="""<h2>The quick way</h2>
<ol><li>Open the <a href="/merge-pdf/">Merge PDF tool</a>.</li><li>Click the box, or drag your PDF files into it.</li><li>Use the arrows to put the files in the order you want.</li><li>Click <strong>Merge PDFs</strong>. The combined file downloads automatically.</li></ol>
<h2>Before you merge: a short checklist</h2>
<ul><li><strong>Name your files in order.</strong> Calling them 01-cover, 02-report and 03-appendix makes the final order easy to check.</li><li><strong>Unlock protected files.</strong> A PDF protected with a password cannot be combined until the password is removed in the program that created it.</li><li><strong>Check page sizes.</strong> Mixing A4 and Letter pages works, but pages will keep their original size in the combined document.</li></ul>
<h2>Common reasons to merge PDFs</h2>
<p>People most often merge PDFs to send one attachment instead of many: a CV and certificates for a job application, a month of invoices for accounting, or chapters of a report written by different people. A single file is easier to review, print and archive.</p>
<h2>Keeping the merged file small</h2>
<p>The merged file is roughly the sum of its parts. If the result is too big to email, run it through the <a href="/compress-pdf/">Compress PDF tool</a>, or reduce the size of the biggest inputs first. Compressing is most effective on scanned pages.</p>
<h2>Fixing mistakes after merging</h2>
<p>If a page ended up in the wrong place, use the <a href="/split-pdf/">Split PDF tool</a> to extract page ranges and merge them again in the right order. If some pages are sideways, the <a href="/rotate-pdf/">Rotate PDF tool</a> can fix that.</p>
<h2>Is it private?</h2>
<p>On EditPDF the merge runs in your browser. Your files are not uploaded to our servers, which makes it suitable for everyday documents. As with any tool, avoid shared computers for confidential files.</p>"""),
 dict(slug="how-to-compress-a-pdf", title="How to Reduce PDF File Size: 5 Practical Ways | EditPDF",
  desc="Five practical ways to make a PDF smaller for email and uploads, from re-saving scans to compressing images. Learn what works and what to expect.",
  h1="How to Reduce PDF File Size: 5 Practical Ways", lead="A PDF that is too big for email or an upload form is a common headache. These methods usually fix it, and you can try them in order.",
  card="Five ways to make a PDF smaller.", tool="compress-pdf", tool_cta="Compress a PDF now",
  body="""<h2>Why PDFs get so large</h2>
<p>Most oversized PDFs are large because of images. A scanned page is a full-resolution photo, and a ten-page scan can easily reach tens of megabytes. Text-only PDFs are usually small.</p>
<h2>1. Compress the PDF</h2>
<p>The fastest fix is the <a href="/compress-pdf/">Compress PDF tool</a>. It re-saves each page as an optimized image. This often shrinks scanned documents dramatically. The trade-off is that text in the new file can no longer be selected or searched, so keep your original.</p>
<h2>2. Scan at a lower resolution</h2>
<p>If you control the scanner, 150 to 200 DPI is enough for reading on screen and keeps files much smaller than 600 DPI. Use black and white or greyscale for plain text documents.</p>
<h2>3. Send only the pages you need</h2>
<p>Use <a href="/split-pdf/">Split PDF</a> to extract the pages that matter. Removing unneeded pages reduces size without touching quality.</p>
<h2>4. Resize photos before you build the PDF</h2>
<p>If you are creating a PDF from pictures with <a href="/image-to-pdf/">Image to PDF</a>, resize very large photos first. A 12-megapixel photo is far bigger than a page needs.</p>
<h2>5. Use your original program's export options</h2>
<p>Word processors and design tools offer a smaller or "minimum size" export setting when saving to PDF. If you still have the source file, this keeps text selectable while compressing images.</p>
<div class="note">Results vary. Text-heavy PDFs may not shrink at all, and the EditPDF compressor will show you the before and after size so you can keep the better version.</div>
<h2>What not to expect</h2>
<p>No tool can make every PDF smaller without any loss. If a file is already compact, there is little left to remove.</p>"""),
 dict(slug="how-to-convert-images-to-pdf", title="How to Convert JPG & PNG Images to PDF (Free) | EditPDF",
  desc="Learn how to turn photos, screenshots and scans into one PDF on any device, with tips on page order, page size and file size.",
  h1="How to Convert JPG & PNG Images to PDF", lead="Photos of documents, screenshots and scans are easier to share as one PDF. Here is how to make it in a minute.",
  card="Turn photos and scans into one PDF.", tool="image-to-pdf", tool_cta="Convert images to PDF",
  body="""<h2>Steps</h2>
<ol><li>Open the <a href="/image-to-pdf/">Image to PDF converter</a>.</li><li>Select your JPG, PNG or WebP images, or drag them in.</li><li>Use the arrows to set the page order.</li><li>Pick a page size: A4, US Letter, or fit to each image.</li><li>Click <strong>Create PDF</strong> and save the file.</li></ol>
<h2>Choosing a page size</h2>
<p><strong>A4 or Letter</strong> suits documents you may print. <strong>Fit to each image</strong> makes every page exactly as large as its picture, which is best for screenshots or artwork.</p>
<h2>Tips for better results</h2>
<ul><li><strong>Photograph documents flat</strong> in good light to avoid shadows and skewed text.</li><li><strong>Check the order</strong> before converting. It is easier than fixing it later.</li><li><strong>Keep photos reasonable in size.</strong> A PDF built from several full-size phone photos can be large.</li></ul>
<h2>Making the PDF smaller</h2>
<p>If the finished PDF is too large to send, use <a href="/compress-pdf/">Compress PDF</a>. For multi-part documents, you can also <a href="/merge-pdf/">merge PDFs</a> created in separate batches.</p>
<h2>Privacy</h2>
<p>Images are converted in your browser and are not uploaded to EditPDF.</p>"""),
]

HOME_FAQ = [
 ("Are these PDF tools really free?","Yes. All EditPDF tools are free to use, with no account, no watermark and no sign-up."),
 ("Are my documents uploaded to a server?","No. Files are processed in your browser. The page loads JavaScript libraries from a public CDN, but your selected files are not sent to those services or to EditPDF."),
 ("Which PDF tools are available?","You can merge PDFs, split and extract pages, rotate pages, compress a PDF, convert images (JPG, PNG, WebP) to PDF, count PDF pages and view PDF properties."),
 ("Will compression always make my PDF smaller?","Not always. The compression tool re-renders pages as images, which helps scanned and image-heavy files but removes selectable text. The tool shows the new size so you can compare."),
 ("Does EditPDF work on phones and tablets?","Yes. The tools run in modern mobile and desktop browsers. Very large files may be slow on older devices."),
 ("Can I convert PDF to Word?","Not yet. Reliable PDF-to-Word conversion needs more advanced processing than the current browser-based tools provide."),
]
