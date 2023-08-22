from flask import Flask, render_template, request,flash,redirect,url_for,abort,send_file
from werkzeug.utils import secure_filename
from tex2lambda.main import runner
from pathlib import Path
import tex2lambda,pkgutil
import os, shutil, tempfile
import fnmatch
import importlib
app = Flask(__name__)
app.config['SECRET_KEY'] = '962d09f8d1d111a49bc7afd4f8e6204cbf2d4e47d30bc3e4'

#get the modules name
modules={
            i.name:(importlib.import_module(f"tex2lambda.filters.{i.name}.filter").__doc__).splitlines()[0]

            for i in pkgutil.iter_modules(tex2lambda.filters.__path__)

            if i.name[0] != "_"

}



    



#create path for the main page
@app.route('/',methods = ['POST','GET'])

def upload_file():
    pattern="*.tex"
    error=None
    if request.method == 'POST':
        f= request.files['file']
        if not f:
            app.logger.info('No file is uploaded')
            error='Please upload a file!'
        else:
            if fnmatch.fnmatch(str(f.filename),pattern):
                f.save(secure_filename(f.filename))
                #Decide on whhich filter to use
                chosenindex=request.form['module']
                app.logger.info(chosenindex)
                #path to take in the files
                path=str(Path(__file__).with_name('Output'))
                #if there is another answer file take the input answer file in
                answer=request.files['answerFile']
                try:
                    if answer:
                            if fnmatch.fnmatch(str(answer.filename),pattern):
                                app.logger.info('With answer')
                                answer.save(secure_filename(answer.filename))
                                runner(f.filename, chosenindex,path,answer.filename)
                            else:
                                error="Please input a valid tex file for answer"
                                if f:
                                    os.remove(f.filename)
                                return render_template('upload.html',modules=modules,error=error)
                        
                    else:
                        runner(f.filename, chosenindex,path) 
                except Exception as e:
                    error="Tex2Lambda reported an error for this filter, the exception is "+str(e)
                    os.remove(f.filename)
                    if answer:
                        os.remove(answer.filename)
                    return render_template('upload.html',modules=modules,error=error)

                if os.path.isdir(path):
                    app.logger.info('Output success')
                    #create large zip folder to output
                    shutil.make_archive(path, "zip", path)  
                    #delete files
                    shutil.rmtree(path)
                    os.remove(f.filename)
                    if answer:
                        os.remove(answer.filename)
                    
                    #setup temporary file to remove file after download
                    cache = tempfile.NamedTemporaryFile()
                    with open("Output.zip", 'rb') as fp:
                        shutil.copyfileobj(fp, cache)
                        cache.flush()
                    cache.seek(0)
                    os.remove("Output.zip")
                    return send_file(cache, as_attachment=True,download_name='Output.zip')
                else:
                    error="The filter you have chosen did not produce any output"
                    #delete import files
                    os.remove(f.filename)
                    if answer:
                        os.remove(answer.filename)
                    return render_template('upload.html',modules=modules,error=error)
            
            error="Please upload a valid tex file. "
            
        return render_template('upload.html',modules=modules,error=error)
    return render_template('upload.html',modules=modules)
	





