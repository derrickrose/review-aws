FROM public.ecr.aws/lambda/python:3.10
COPY lambda_watermark.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["lambda_watermark.lambda_handler"]