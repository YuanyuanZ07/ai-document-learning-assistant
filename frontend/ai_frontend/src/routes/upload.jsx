import { useState } from 'react';
const Upload = () => {
    const [file , setfile] = useState(null);  

    const handleFileChange = (event) => {
        setfile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        if (!file) {
            alert('Please select a file to upload.');
            return;
        }

        event.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
        const response = await fetch(`${process.env.API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
        
        });

        if (response.ok) {
        // Handle success (e.g., show a success message)
        console.log('File uploaded successfully!');
        } else {
        // Handle errors
        console.error('Upload failed.');
        }
    } catch (error) {
        console.error('Error during upload:', error);
    }
    };
   
    
    return (
        <div className="min-h-screen bg-darkgray-100 flex flex-col items-center justify-center p-4">
            <h1 className="text-4xl font-bold mb-6 text-center">Upload a File</h1>
            <form onSubmit={handleSubmit}>
                <input className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" type="file" onChange={handleFileChange} />
                <button >Upload</button>
            </form>
        </div>
    );
};
export default Upload;