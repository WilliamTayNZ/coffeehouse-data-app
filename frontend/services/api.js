const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function loadExistingFiles() {
    const res = await fetch(`${BASE_URL}/api/load_existing`);
    if (res.ok) return res.json();
    throw new Error('Failed to load files');
  }

export async function uploadFile(file) {
  const formData = new FormData();
  console.log(file);
  formData.append('file', file);

  console.log("Uploading to:", `${BASE_URL}/api/upload`);
  const res = await fetch(`${BASE_URL}/api/upload`, {method: 'POST', body: formData});
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || 'Failed to upload file');
  }
  return res.json();
}

export async function previewFile(filename) {
  const res = await fetch(`${BASE_URL}/api/preview_uncleaned_file/${encodeURIComponent(filename)}`);
  const data = await res.json();
  if (!res.ok || data.error) throw new Error(data.error || 'Failed to preview file');
  return data;
}

export async function cleanFile(fileOrFilename) {
  if (fileOrFilename instanceof File) {
    // Uploaded File object
    const formData = new FormData();
    formData.append('file', fileOrFilename);
    const res = await fetch(`${BASE_URL}/api/clean_file`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to clean file');
    }
    return res.json();

  } else if (typeof fileOrFilename === 'string') { 
    // Existing filename
    const res = await fetch(`${BASE_URL}/api/clean_file`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename: fileOrFilename }),
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to clean file');
    }
    return res.json();
  } else {
    throw new Error('Invalid cleanFile argument');
  }
}